import sys

class Logger:
    def process_exception(self, request, exception):
        sys.stdout.write(str(exception) + '\n')
        raise exception
        
        