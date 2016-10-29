import xml.etree.cElementTree as ET 
import sys
import getopt
import html.parser
import re
import os
import io

#_min_score = 1 
#_min_view_count = 1000
#_min_answer_count = 2
_output_dir = 'output'


_write = False
_attrs_min_values = {}
_attrs_required_names = []
_attrs_eq_values = {}
#def PrintUsage(str):


def WriteToFile(result, output_dir):

  print ('start to writing files.')

  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  file_count = 0
  bodys = []
  parser = html.parser.HTMLParser()
  dr = re.compile(r'<[^>]+>',re.S)
  for child in result:
    postbody = parser.unescape(child.attrib['Body'])
    postbody = dr.sub('', postbody)  
    postid = parser.unescape(child.attrib['Id'])
    fileobj = io.open(output_dir + '\\'+postid + '.txt', 'w', encoding='utf-8')
    fileobj.write('\n')
    try:
      fileobj.write(postbody)
    except Exception as e:
      print ('postid: ' + postid)
      print (str(e))
      print (postbody[0:100])
      sys.exit()
    
    fileobj.write('\n')
    file_count = file_count +1
    if file_count % 100 == 0:
      print (str(file_count) + ' files has been created.')

  print ('finally, 'str(file_count) + ' files has been created.')



def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 
                                                 'min_score=',
                                                 'min_view_count=',
                                                 'min_answer_count=',
                                                 'has_accepted_answer_id'
                                                 'post_type_id='
                                                 'write'
                                                 'output_dir=',
                                                 ]) 
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')

  global _attrs_min_values
  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--write':
      global _write = True
    elif opt == '--post_type_id':
      _attrs_eq_values['PostTypeId'] = val
    elif opt == '--has_accepted_answer_id':
      _attrs_required.append('AcceptedAnswerId')
    elif opt == '--min_answer_count':
      _attrs_min_values['AnswerCount'] = int(val)
    elif opt == '--min_score':
      _attrs_min_values['Score'] = int(val)
    elif opt == '--min_view_count':
      _attrs_min_values['ViewCount'] = int(val)
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
    qualified = True 
    for (attr_name, min_value) in _attrs_min_values.items():
      if not attr_name in child.attrib:
        qualified = False
        break
      if childl.attrib[attr_name] < min_value:
        qualified = False
        break
  
    if not qualified:
      continue

    for attr_name in _attrs_required:
      if not attr_name in child.attrib:
        qualified = False
        break

    if not qualified:
      continue

    for (attr_name, eq_value) in _attrs_eq_values.items():
      if not attr_name in child.attrib:
        qualified = False
        break
      if childl.attrib[attr_name] != eq_value:
        qualified = False
        break
      
    if not qualified:
      continue
    
    result.append(child)


        
  #print ('Score >= ' + str(_min_score) + ' and ViewCount >= ' + str(_min_view_count) + ' and AnswerCount >= ' + str(_min_answer_count) +':\n')
  print ('qualified item count: ' + str(len(result)))

 
  WriteToFile(result, _output_dir)

