import xml.etree.cElementTree as ET 

import cgi
import copy
import sys
import getopt
import html.parser
import re
import os
import io
import time

import xml.sax
import xml.sax.handler

  


_write = False
_output_dir = 'output'
_file_path = 'Posts.xml'

_file_prefix = None
#_digit_capa = 5



_orderby_attr_name = None
_top = None


_attrs_min_values = {}
_attrs_required_names = []
_attrs_eq_values = {}

def PrintUsage(str):
  print(str)

def Order(item_list, attr, top_count):


  print ('start to order')
  sys.stdout.flush()
  checked_count = 0
  backets = {}
  for child in result:
    number = int(child.attrib[attr])
    if number in backets:
      backets[number] = backets[number] + 1
    else:
      backets[number] = 1
    checked_count = checked_count + 1
    if checked_count % 10000 == 0:
      print (str(checked_count) +' items checked (ordering)')
      sys.stdout.flush()


  for (number, count) in backets.items():
    print (_orderby_attr_name + ' = ' + str(number) +' : ' + str(count))

  left_count = top_count 
#  while (Left_count > 0):


def Filter(root):
 
  checked_count = 0
  result = []
  for child in root:
    checked_count = checked_count + 1
    if(checked_count % 10000 == 0):
      print (str(checked_count) +' items checked')
      sys.stdout.flush()
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

  #print ('qualified item count: ' + str(len(result)))
  #sys.stdout.flush()
  return result

def WriteToFile(result, output_dir):

  print ('start to writing files.')

  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  file_count = 0
  bodys = []
  parser = html.parser.HTMLParser()
  dr = re.compile(r'<[^>]+>',re.S)
  for child in result:
    postbody = child.attrib['Body']
    #postbody = parser.unescape(child.attrib['Body'])
    #postbody = dr.sub('', postbody)  
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
      sys.stdout.flush()

  print ('finally, ' + str(file_count) + ' files has been created.')



def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 
                                                 'min_Score=',
                                                 'min_ViewCount=',
                                                 'min_AnswerCount=',
                                                 'has_AcceptedAnswerId',
                                                 'eq_PostTypeId=',
                                                 'orderby=',
                                                 'top=',
                                                 'write',
                                                 'output_dir=',
                                                 'file_path=',
                                                 'file_prefix='
                                                 ]) 
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')
    
  global _attrs_min_values
  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--orderby':
      global _orderby_attr_name
      _orderby_attr_name = val
      _attrs_required_names.append(val)
    elif opt == '--top':
      global _top
      _top = int(val)
    elif opt == '--file_prefix':
      global _file_prefix
      _file_prefix = val
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


class Element:
  def __init__(self):
    self.attrib = {}
    self.row_index = 0


class DataHandler( xml.sax.ContentHandler ):
  def __init__(self, result, filter_func):
    self.result = result
    self.parsed_items_count = 0 
    #self.element = Element()
    self.filter_func = filter_func
    global _file_path
    print ('1')
    sys.stdout.flush()
    self.infile = open(_file_path, 'r', encoding='utf8')
    self.inlines = self.infile.readline()
    self.inlines = self.infile.readline()
    print ('2')
    sys.stdout.flush()
    self.parsing_row_index = 2 
    self.outfile = open('filtered.xml', 'w', encoding='utf8')
    
    self.attr_names = ['PostTypeId', 'Score', 'ViewCount', 'AnswerCount', 'AcceptedAnswerId']

  # 元素开始事件处理
  def startElement(self, tag, attributes):
    if tag == "row":

      sys.stdout.flush()
      self.inlines = self.infile.readline()
      element = Element()
      '''
      for (attr_name, value) in attributes.items():
        self.element.attrib[attr_name] = value 
      '''

      for attr_name in self.attr_names:
        if attr_name in attributes:
          element.attrib[attr_name] = attributes[attr_name]

      filtered_items = self.filter_func([element])
      if len(filtered_items) > 0:
        self.outfile.write(self.inlines) 
      
      self.parsed_items_count = self.parsed_items_count + 1
      if self.parsed_items_count % 1000 == 0:
        print ('%d items has been parsed' % self.parsed_items_count)
        sys.stdout.flush()
      #self.parsing_row_index = self.parsing_row_index + 1

  # 元素结束事件处理
  def endElement(self, tag):
    return
    self.parsed_items_count = self.parsed_items_count + 1
    if self.parsed_items_count % 10000 == 0:
      print ('%d items has been parsed' % self.parsed_items_count)
      print ('%d items in the result' % len(self.result))
      sys.stdout.flush()

    '''
    print ('body------')
    print (self.element.attrib['Body'])
    sys.stdout.flush()
    '''

    if self.filter_func != None:
      filtered_items = self.filter_func([self.element])
      if len(filtered_items) == 0:
        return

   
    self.result.append(self.element)

  def endDocument(self):
    print ('document parsed finished')
  #  print ('%d items in the result' % len(self.result))
    self.infile.close() 
    self.outfile.close() 
  
  # 内容事件处理
  #def characters(self, content):


def WriteElementsToCSV(elements, file_path):
  if len(elements) == 0:
    return;
 
  print(' start to write elements to csv.')
  sys.stdout.flush()
  
  outfile = open(file_path, 'w', encoding='utf-8')
  #outfile = open(file_path, 'wb')
  title_str = ''

  for attr_name in elements[0].attrib:
    outfile.write(attr_name + ',')
  outfile.write('\n')

  for element in elements:

    #print (element.attrib['Body'])
    sys.stdout.flush()
    for (attr_name, value) in element.attrib.items():
      parser = html.parser.HTMLParser()
      content = (cgi.escape(value))
      outfile.write(content + ',')
    outfile.write('\n')
  
  outfile.close()
  print ('write finished')
  sys.stdout.flush()

def ExtractLinesToFile(original_file_path, filtered_file_path, filetered_result):
  infile = open(original_file_path, 'r', encoding='utf8')
  outfile = open(filtered_file_path, 'w', encoding='utf8')
  in_line_index = -1
  result_count = len(result)
  result_index = 0

 

  line = infile.readline() #skip xml head 
  line = infile.readline() #skip '<posts>'

  writen_lines_count = 0
  while True:
    line = infile.readline()
    in_line_index = in_line_index + 1
    if not line:
      break
    if(in_line_index != result[result_index].row_index):
      continue
    else:
      outfile.write(line)
      writen_lines_count = writen_lines_count + 1
      if writen_lines_count % 10000 == 0:
        print ('%d lines has been writen' % writen_lines_count) 
      result_index = result_index + 1
      if result_index == result_count:
        break
        

      
  print ('finally:::::%d lines has been writen' % writen_lines_count) 
  infile.close()
  outfile.close()


if (__name__ == '__main__'):
  print ('start')
  ParseArgs(sys.argv[1:])

  

  result = []
  root = [] 

  print ('start to parse the xml file')
  sys.stdout.flush()
  try:
    global _file_prefix
    if _file_prefix != None:
      file_parsed_count = 0
      for i in range(3, 1000):
        each_file_path = _file_prefix + ('%.5d' % i)
        if not os.path.exists(each_file_path):
          break;
        infile = open(each_file_path, 'r', encoding='utf-8')
        content = infile.read()
        print ('parsing ' + each_file_path)
        sys.stdout.flush()

#xml parse
        xml.sax.parseString(content, DataHandler(root))
        #root = ET.fromstring('<posts>' + content + '</posts>')

        print ('parse succeed %d items' % len(root) )
        sys.stdout.flush()

        items = Filter(root)
        result.extend(items)
      print ('%d files has been parsed' % file_parsed_count)
      print ('%d items in filtered result' % len(result)) 
      #infile = open(
    else:
      global _file_path
      
      '''
      infile = open(_file_path, 'r', encoding='utf8')
      content = infile.read()
      xml.sax.parseString(content, DataHandler(result, Filter))
      '''
          
      xml.sax.parse(_file_path, DataHandler(result, Filter))
      ''' 
      tree = ET.parse(_file_path)
      root = tree.getroot()
      #WriteToFile(root[0:5], _output_dir)
      infile = open('test.txt', 'w')
      #infile.write(root[2].attrib['Body'])
      infile.close()
      print ('bbbbbbb--------')
      print (cgi.escape(root[2].attrib['Body']).encode('utf8'))
      #result = Filter(root) #filter
      '''
  except IOError as e:
    
    print ("parse error or file not found")
    print ("msg: "+ str(e))
    sys.stdout.flush()
    sys.exit(1)
  
 
  print ('parse the xml file finished')
#write
  global _write
 # if _write:
    #ExtractLinesToFile(_file_path, 'filtered.xml', result)
  
    #WriteElementsToCSV(result, 'filterd.csv')

    #WriteToFile(result, _output_dir)


  ''' 
#order
  if _orderby_attr_name != None:
    Order(result, _orderby_attr_name, _top)


#write
  global _write
  if _write:
    WriteToFile(result, _output_dir)
  '''
