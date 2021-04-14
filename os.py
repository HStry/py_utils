def which(command, cwd=False):
  if not isinstance(command, str):
    raise TypeError('command must be a string')
  if not command:
    raise ValueError('command invalid')
  
  win = os.name == 'nt'
  sep = ';' if win else ':'
  
  paths = [p.strip()
           for p in os.getenv('PATH').split(sep)
           if p.strip() and os.path.isdir(p.strip())]
  
  if cwd:
    paths.insert(0, os.getcwd())
  
  if not win:
    match = lambda p, f: (command == f and
                          os.path.isfile(p + os.sep + f) and
                          os.stat(p + os.sep + f).st_mode &
                          os.path.stat.S_IXUSR)
  
  else:
    command = command.lower()
    exts = tuple(e.lower().strip()
                 for e in os.getenv('PATHEXT').split(sep)
                 if e.strip())
    if command.endswith(exts):
      match = lambda p, f: command == f.lower()
    else:
      def match(p, f):
        f, e = os.path.splitext(f.lower())
        return (command == f and e in exts and
                os.path.isfile(p + os.sep + f + e))
  
  return [path + os.sep + file
          for path in paths
          for file in os.listdir(path)
          if match(path, file)]
