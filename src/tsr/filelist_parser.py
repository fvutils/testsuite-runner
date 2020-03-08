'''
Created on Nov 23, 2019

@author: ballance
'''

import os

class FilelistParser():
    
    class Token():
        def __init__(self, 
                     parser,
                     fileid,
                     img, 
                     lineno,
                     linepos):
            self.parser = parser
            self.img = img
            self.fileid = fileid
            self.lineno = lineno
            self.linepos = linepos
            
        def get_img(self, expand_env=False):
            if expand_env:
                return self.expand(self.img)
            else:
                return self.img
            
        def expand(self, str):
            i=0
            ret = ""
            while i < len(str):
                d_idx = str.find('$', i)
                if d_idx != -1:
                    ret += str[i:d_idx]
                    if str[d_idx+1] == '{':
                        c_idx = str.find('}', d_idx+2)
                        if c_idx != -1:
                            key = str[d_idx+2:c_idx]
                            if key in os.environ:
                                ret += os.environ[key]
                            i = c_idx+1
                        else:
                            ret += str[d_idx+1]
                            i = d_idx+2
                    else:
                        ret += str[i+1]
                        i += 1
                else:
                    ret += str[i:]
                    break
            return ret
    
    class Input():
        def __init__(self, parser, fileid, fp):
            self.parser = parser
            self.fileid = fileid
            self.fp = fp
            self.lineno = 1
            self.linepos = 1
            self.last_c = b''
            self.unget_c = b''
            pass
        
        def __iter__(self):
            return self
        
        def __next__(self):
            tok = self.readtok()
            
            if tok == None:
                raise StopIteration
            
            return FilelistParser.Token(
                self.parser,
                self.fileid,
                tok[0],
                tok[1],
                tok[2]
                )
            
            # 
            return self.read_tok()
        
        def readtok(self):
            ch=b''
            ch2=b''
            ret=""
            start_lineno = -1
            start_linepos = -1
            
            while True:
                ch = self.getch()
                if ch == b'':
                    break
                
                if (ch == b'/'):
                    ch2 = self.getch()
                    if ch2 == b'*':
                        cc1 = b''
                        cc2 = b''
                        
                        while True:
                            ch = self.getch()
                            if ch == b'':
                                break
                            cc2 = cc1
                            cc1 = ch
                            if cc1 == b'/' and cc2 == b'*':
                                break
                        continue
                    elif ch2 == b'/':
                        while True:
                            ch = self.getch()
                            if ch == b'' or ch == b'\n':
                                break
                        self.ungetch(ch)
                        continue
                    else:
                        self.ungetch(ch2)
                elif ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r':
                    while True:
                        ch = self.getch()
                        if ch == b'' or not (ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r'):
                            break
                    self.ungetch(ch)
                    continue
                else: # Actually a non-whitespace/non-comment character
                    start_lineno = self.lineno
                    start_linepos = self.linepos
                    break
                
            while ch != b'' and not (ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r'):
                ret += ch.decode("utf-8")
                ch = self.getch()
            self.ungetch(ch)
            
            if ret == "":
                return None
            else:
                return (ret, start_lineno, start_linepos)
        
        def getch(self):
            ch = b''
            if self.unget_c != b'':
                ch = self.unget_c
                self.unget_c = b''
            else:
                ch = self.fp.read(1)
                if self.last_c == b'\n':
                    self.linepos = 1
                    self.lineno += 1
                else:
                    self.linepos += 1
                    
                self.last_c = ch
                
            return ch
        
        def ungetch(self, c):
            self.unget_c = c
        
    def __init__(self):
        self.filename_l = []
        self.filename_m = {}
        self.input_s = []
        self.token_l = []
        self.fail_on_error = False
        self.backtrace_on_error = False
        self.expand_env = True
        
    def set_fail_on_error(self, f):
        self.fail_on_error = f
        
    def set_backtrace_on_error(self, f):
        self.backtrace_on_error = f
        
    def set_expand_env(self, e):
        self.expand_env = e
        
    def error(self, msg):
        print("Error: " + msg)
        if self.fail_on_error:
            raise Exception(msg)
        
    def warning(self, msg):
        print("Warning: " + msg)
        
    def parse(self, path, relative_path_basedir):
        if not os.path.exists(path):
            self.error("path \"" + path + "\" does not exist")
            return
        
        # TODO: prevent recursion
        
        try:
            fp = open(path, "rb")
        except Exception as e:
            self.error("failed to read file \"" + path + "\" (" + str(e) + ")")
            pass
            return
        
        fileid = len(self.filename_l)
        self.filename_l.append(path)
        self.filename_m[path] = fileid
        
        input = FilelistParser.Input(self, fileid, fp)
        self.input_s.append(input)
        
        # Now, process content until we're done
        it = iter(input)
        while True:
            try:
                tok = next(it)
            except StopIteration:
                break
                pass
            
            if tok.img == "-f" or tok.img == "-F":
                # Sub-inclusion
                try:
                    tok = next(it)
                except StopIteration:
                    break
                    pass
                
                self.parse(tok.get_img(True), relative_path_basedir)
            else:
                self.token_l.append(tok)
        
        self.input_s.pop()
            
        pass
    
    