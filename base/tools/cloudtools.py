import re, types, math
from porter import PorterStemmer
from django.template.loader import render_to_string

class InvalidInputException(Exception):
    pass

class TagCloudMaker:
    def __init__(self, text):
        self.text = text
        
    def extract_quotes(self):
        quotes = re.findall('"([^"]*)"', self.text)
        if quotes:
            return quotes
        else:
            return list(self.text)

    def process_cloud(self, steps, input):
        if not type(input) == types.ListType or len(input) <= 0 or steps <= 0:
            raise InvalidInputException,\
              "Please be sure steps > 0 and your input list is not empty."
        else:
           temp, newThresholds, results = [], [], []
           for item in input:
               if not type(item) == types.TupleType:
                   raise InvalidInputException, "Be sure input list holds tuples."
               else: temp.append(item[1])
           maxWeight = float(max(temp))
           minWeight = float(min(temp))
           newDelta = (maxWeight - minWeight)/float(steps)
           for i in range(steps + 1):
              newThresholds.append((100 * math.log((minWeight + i * newDelta) + 2), i))
           for tag in input:
               fontSet = False
               for threshold in newThresholds[1:int(steps)+1]:
                   if (100 * math.log(tag[1] + 2)) <= threshold[0] and not fontSet:
                       results.append({'tag': tag[0], 'count':str(threshold[1])})
                       fontSet = True
        return results

    def make_cloud(self):
        stemdict, tempdict, finaldict = {}, {}, {}
        stopwords = open('/home/politicsv/django-projects/politicsverbatim/base/tools/stopwords.txt', 'r').read().split('\n')

        # Extract just the words inside quotes
        quotes = ' '.join(self.extract_quotes())
        wordlist = re.split('\s+', quotes.lower())
        
        p = PorterStemmer()
        punctuation = re.compile(r'[.?!,":;-]')

        # Stem all of the words in the word list using the Porter Stemmer
        for w in wordlist:
            w = punctuation.sub('', w)
            s = p.stem(w, 0,len(w)-1)
            try:
                tempdict[w] += 1
            except:
                tempdict[w] = 1
            stemdict.setdefault(s,{}).update({w:tempdict[w]})
        
        cumfreq = 0

        # Calculate the cumulative frequencies of the stemmed words
        for k, v in stemdict.items():
            for l, m in v.items():
                cumfreq = cumfreq + m
            items = v.items()
            items.sort(lambda x, y: cmp(y[1], x[1]))
            finaldict[items[0][0]] = cumfreq
            cumfreq = 0

        # Remove stopwords like "the", "it", "a", etc.
        for word in stopwords:
            try:
                del finaldict[word]
            except: pass

        results = self.process_cloud(8, finaldict.items()[:50])
        return results


    def make_cloud_template(self):
        results = self.make_cloud()
        return render_to_string('base/includes/tagcloud.html', {'tags': results})
