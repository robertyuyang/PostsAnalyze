import xml.etree.cElementTree as ET 
import sys
import getopt
import html.parser
import re
import os

_min_score = 1 
_min_view_count = 1000
_min_answer_count = 2
_output_dir = 'output'

#def PrintUsage(str):



def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 
                                                 'min_score=',
                                                 'min_view_count=',
                                                 'min_answer_count=',
                                                 'output_dir='
                                                 ]) #added by Robert
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')
  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--min_answer_count':
      global _min_answer_count
      _min_answer_count = int(val)
    elif opt == '--min_score':
      global _min_score
      _min_score = int(val)
    elif opt == '--min_view_count':
      global _min_view_count
      _min_view_count = int(val)
    elif opt == '--output_dir':
      global _output_dir
      _output_dir = val


if __name__ == '__main__':

  ParseArgs(sys.argv[1:])

  

  try:
    tree = ET.parse('Posts.xml')
    root = tree.getroot()
  except Exception :
    print ("parse error")
    sys.exit(1)
  
  
  result = []
  for child in root:
    if 'Score' in child.attrib and 'ViewCount' in child.attrib and 'AnswerCount' in child.attrib:
      if int(child.attrib['Score']) >= _min_score and int(child.attrib['ViewCount']) >= _min_view_count and int(child.attrib['AnswerCount']) >= _min_answer_count:
        if 'Body' in child.attrib:
          result.append(child)
        
  print ('Score >= ' + str(_min_score) + ' and ViewCount >= ' + str(_min_view_count) + ' and AnswerCount >= ' + str(_min_answer_count) +':\n')
  print (len(result))

  if not os.path.exists(_output_dir):
    os.mkdir(_output_dir)

  file_count = 0
  bodys = []
  parser = html.parser.HTMLParser()
  dr = re.compile(r'<[^>]+>',re.S)
  for child in result:
    postbody = parser.unescape(child.attrib['Body'])
    postbody = dr.sub('', postbody)  
    postid = parser.unescape(child.attrib['Id'])
    fileobj = open(_output_dir + '\\'+postid + '.txt', 'w')
    fileobj.write('\n')
    fileobj.write(postbody)
    fileobj.write('\n')
    file_count = file_count +1
    if file_count == 10:
      break
  print (str(file_count) + ' files has been created.')



