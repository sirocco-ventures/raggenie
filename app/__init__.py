# # these three lines swap the stdlib sqlite3 lib with the pysqlite3 package
# https://docs.trychroma.com/troubleshooting#sqlite
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')