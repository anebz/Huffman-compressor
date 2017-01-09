# Imports
import operator
import json
import ast

# Global Variables
zeros = 0

# should be a .txt
def readfile(filename):
  return open(filename, encoding='utf-8').read()

def writefile(filename, tree, string):
  f = open(filename, 'w', encoding='utf-8')
  json.dump(tree, f) # dump tree
  f.write(string)
  f.close()

# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in range(127):
    if string.count(chr(i)):
      freq[chr(i)] = string.count(chr(i))*1.0/leng
  if string.count('’'):
    freq['’'] = string.count('’')*1.0/leng
  return freq

# returns a list with the Huffman-encoded ASCII table
def constructHuffmanTree(text, count):
  savedCoding = dict.fromkeys(count.keys(), '')
  aux = dict(count)
  for ii in range(len(count) - 1):
    flag = 0
    dictValues = list(aux.values())
    smallestElementValue = min(dictValues)
    secondSmallestElementValue = second_smallest(dictValues)
    for key,value in aux.items():
      if value == smallestElementValue or value == secondSmallestElementValue:
        flag += 1
        if flag == 1:
          node1 = key
          for jj in key:
            savedCoding[jj] = '0' + savedCoding[jj]
        elif flag == 2:
          node2 = key
          for jj in key:
            savedCoding[jj] = '1' + savedCoding[jj]
          break
    aux[node1] = aux[node1] + aux[node2]
    newLetter = node1 + node2
    aux[newLetter] = aux[node1]
    del aux[node1]
    del aux[node2]
  return savedCoding

# given a tree in this format: {0:'a', 10:'b', 11:'c'}
# and words being the string read from the file
def encode(tree,words):
  #inv_tree = {value:key for key,value in tree.items()}
  code = ''
  for let in words:
    if let in tree:
      code = code + str(tree[let])
  return code

def code_to_string(code):
  global zeros 
  zeros = len(code)%8
  compressed = ''
  if zeros != 0: # not a multiple of 8
    code = code + '0'*zeros # add zeroes, redundancies
  for i in range(0,len(code),8):
    compressed = compressed + chr(int(code[i:i+8],2))
  return compressed

#Decoding function
def decode(tree2, code):
  tree = {value:key for key,value in tree2.items()}
  text,add = '',''
  for i in range(len(code)):    
    add += code[i]
    if add in tree.keys():
      text += tree[add]
      add = ''
  return text

# returns the second smallest element in a numeric list
def second_smallest(numbers):
  return sorted(numbers,key=float)[1]

def string_to_code(text):
  code = ''
  for e in text:
    code += "{0:b}".format(ord(e))
  return code
   
  
  
##ENCODING

# open file
file = 'text_sample.txt'
original_text = readfile(file)

#Constructing the tree
characterCounter = frequency(original_text)
tree = constructHuffmanTree(original_text, characterCounter)
print(tree)

# example cases for encoding
#tree = {0:'a', 10:'b', 11:'c'}
words = original_text
#words = 'acbcab' 
code = encode(tree,words)
#print (code)

compressed = code_to_string(code)
#print(compressed)

print(len(original_text),len(compressed))

print("Compresion rate:", len(compressed)/len(original_text))

# write in file
extension = 'hff'
ex_filename = 'result' + '.' + extension
tree['999'] = zeros
writefile(ex_filename, tree, compressed)

## DECODING
file = 'result.hff'
text2 = readfile(file)
tree2 = ast.literal_eval(text2[:text2.find('}')+1])
#print(tree2)
zeros2 = tree2['999']

text2 = text2[text2.find('}'):(len(text2)-zeros2+1)] # the encoded text
code2 = string_to_code(text2)

decoded = decode(tree2, code)

print(len(decoded),len(original_text))

f = open('decoded.txt', 'w', encoding='utf-8')
f.write(decoded)
f.close()

for i in range(len(original_text)):
  if decoded[i] != original_text[i]:
    print(i,decoded[i],original_text[i])
    break


