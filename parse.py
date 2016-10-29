import xml.etree.cElementTree as ET 
import sys
import getopt
import html.parser
import re
import os
import io

_write = False
_output_dir = 'output'
_file_path = 'Posts.xml'


_attrs_min_values = {}
_attrs_required_names = []
_attrs_eq_values = {}

def PrintUsage(str):
  print(str)

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

  print ('finally, ' + str(file_count) + ' files has been created.')



def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 
                                                 'min_Score=',
                                                 'min_ViewCount=',
                                                 'min_AnswerCount=',
                                                 'has_AcceptedAnswerId',
                                                 'eq_PostTypeId=',
                                                 'write',
                                                 'output_dir=',
                                                 'file_path='
                                                 ]) 
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')
    
  global _attrs_min_values
  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--file_path':
      global _file_path
      _file_path = val
    elif opt == '--write':
      global _write
      _write = True
    elif opt == '--eq_PostTypeId':
      _attrs_eq_values['PostTypeId'] = val
    elif opt == '--has_AcceptedAnswerId':
      _attrs_required_names.append('AcceptedAnswerId')
    elif opt == '--min_AnswerCount':
      _attrs_min_values['AnswerCount'] = int(val)
    elif opt == '--min_Score':
      _attrs_min_values['Score'] = int(val)
    elif opt == '--min_ViewCount':
      _attrs_min_values['ViewCount'] = int(val)
    elif opt == '--output_dir':
      global _output_dir
      _output_dir = val


if __name__ == '__main__':
  ParseArgs(sys.argv[1:])

  

  try:
    global _file_path
    tree = ET.parse(_file_path)
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

    for attr_name in _attrs_required_names:
      if not attr_name in child.attrib:
        qualified = False
        break

    if not qualified:
      continue

    for (attr_name, eq_value) in _attrs_eq_values.items():
      if not attr_name in child.attrib:
        qualified = False
        break
      if not child.attrib[attr_name] == eq_value:
        qualified = False
        break
      
    if not qualified:
      continue
    
    result.append(child)


        
  print ('qualified item count: ' + str(len(result)))


  global _write
  if _write:
    WriteToFile(result, _output_dir)

