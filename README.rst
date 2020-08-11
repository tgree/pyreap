pyreap
======
This module provides a subprocess.Popen()-compatible reap.Popen() function that
has the nice property that if the parent process dies the child process will
also be reaped.

Normally, orphaned child processes will end up re-parented to the init(1)
process and then live on until they finally complete of their own volition.  
This often (usually?) isn't the desired behavior and it can be really handy to
ensure that when a parent process dies all the child processes will be
automatically cleaned up.

The reap module accomplishes this by inserting a small intermediate process
between the parent and the child.  This intermediate process periodically
checks to see if its parent PID has changed (indicating that the parent died
and we have been reparented to init(1) or some other init(1)-like process), and
if a change is detected then it kills the child before itself exiting.  This
ensures that any child processes you create will not later live on as orphaned
processes.

Using pyreap is as easy as using subprocess.Popen(), and in fact all arguments
are simply passed to subprocess.Popen(); the reap.Popen() function also returns
a subprocess.Popen object that you can use just like you normally would.

The following demonstrates how subprocess.Popen() behaves with an orphaned
process (note the orphaned 'sleep 1000' lives on even after the Python
interpreter has closed)::

    ~$ python3
    Python 3.8.5 (default, Jul 21 2020, 10:48:26)
    [Clang 11.0.3 (clang-1103.0.32.62)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import subprocess
    >>> subprocess.Popen(['/usr/bin/env', 'sleep', '1000'])
    <subprocess.Popen object at 0x10fc67d30>
    >>>
    ~$ ps aux | grep sleep
    greent7          85310   0.0  0.0  4268280    656 s026  S+    4:57pm   0:00.01 grep sleep
    greent7          85308   0.0  0.0  4268156    504 s026  S     4:57pm   0:00.01 sleep 1000

The following demonstrates how reap.Popen() solves the orphan issue::

    greent7@avocado:~$ python3
    Python 3.8.5 (default, Jul 21 2020, 10:48:26)
    [Clang 11.0.3 (clang-1103.0.32.62)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import reap
    >>> reap.Popen(['/usr/bin/env', 'sleep', '1000'])
    <subprocess.Popen object at 0x10bac9d30>
    >>>
    greent7@avocado:~$ ps aux | grep sleep
    greent7          85319   0.0  0.0  4287736    704 s026  S+    4:57pm   0:00.01 grep sleep

Note how the 'sleep 1000' process is reaped after the Python interpreter shuts
down.
