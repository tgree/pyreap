import argparse
import sys
import os

import reap


def main_parent():
    # Find the path to our script, which we will re-exec with --wfd.
    fp       = os.path.realpath(__file__)

    # Create a pipe.
    rfd, wfd = os.pipe()
    f        = os.fdopen(rfd, 'r')

    # Spawn the child and pass the wfd number to the child.
    cmd      = [sys.executable, fp, '--wfd', '%u' % wfd]
    proc     = reap.Popen(cmd, pass_fds=(wfd,))

    # Close the wfd in the parent here; if we don't close it then we won't get
    # EOF on the pipe when the child terminates because we'll still have a
    # writeable pipe end dangling here.
    os.close(wfd)

    # Read and echo all data from the child.
    data = f.read()
    print(data)

    # Clean up the child process.
    proc.communicate()
    print('Exited with code: %d' % proc.returncode)


def main_child(wfd):
    # Simply wrap wfd in a text-mode file object and write to it.
    f = os.fdopen(wfd, 'w')
    f.write('Hello, world!')


def main(args):
    if args.wfd:
        main_child(args.wfd)
    else:
        main_parent()


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wfd', type=int)

    try:
        main(parser.parse_args())
    except KeyboardInterrupt:
        print()
        pass


if __name__ == '__main__':
    _main()
