import pickle
import argparse
import sys

parser = argparse.ArgumentParser(description='Process query request about NDS dynamic attributes and its properties.')
parser.add_argument("-p", "--primary_role_only", action="store_true", help="display only primary attributes")
parser.add_argument("-s", "--secondary_role_only", action="store_true", help="display only secondary attributes")
parser.add_argument("-a", "--all_properties", action="store_true", help="display all kinds of attributes, cannot combined with 'primary/secondary' options")
parser.add_argument("-r", "--related_features", nargs=1, metavar='features', help="toggle to display related features")
parser.add_argument("attribute_name", nargs='?', help="attribute name to display its properties")
args = parser.parse_args()

attribute_name = ""
primary = 0
features = 0
flist = []

# load data structure from file
f = open('./ndsattribs.pickle', 'rb')
d = pickle.load(f)
f.close()

if args.primary_role_only:
    # print("role base")
    primary = 1
if args.secondary_role_only:
    # print("role base")
    primary = 2
if args.all_properties:
    primary = 3
    if args.primary_role_only or args.secondary_role_only:
        print("show all properties cannot be combined with 'primary only' and 'secondary only' options, exit")
        sys.exit(1)
# not yet used
if args.related_features:
    rf = str(args.related_features[0])
    for word in d:
        for word1 in d[word]:
            for word2 in d[word][word1]:
                if rf in word2:
                    features = 1
                    break
    if features == 0:
        print("1 no such features is exist, check the name carefully (typo)")
        sys.exit(0)

# when attribute name is specified
if args.attribute_name:
    attribute_name = args.attribute_name
    if attribute_name not in d:
        print("no such attribute is exist, check the name carefully (typo)")
        sys.exit(0)
    if primary == 1:
        if d[attribute_name].get("PRIMARY"):
            print(d[attribute_name])
        else:
            print(attribute_name, " is not a primary attributes")
    elif primary == 2:
        if d[attribute_name].get("SECONDARY"):
            print(d[attribute_name])
        else:
            print(attribute_name, " is not a secondary attributes")
# no attribute name is specified
else:
    if primary == 1:
        for word in d:
            if d[word].get("PRIMARY"):
                if features == 1:
                    for c in d[word].get("PRIMARY"):
                        if rf in c:
                            print(word, d[word].get("PRIMARY"))
                            break;
                        else:
                            pass
                else:
                    print(word, d[word].get("PRIMARY"))
        sys.exit(0)
    if primary == 2:
        for word in d:
            if d[word].get("SECONDARY"):
                if features == 1:
                    for c in d[word].get("SECONDARY"):
                        if rf in c:
                            print(word, d[word].get("SECONDARY"))
                            break;
                        else:
                            pass
                            # print("no related features for [", rf, "] is available")
                else:
                    print(word, d[word].get("SECONDARY"))
        sys.exit(0)
    if primary == 3:
        for word in d:
            if features == 1:
                for c in d[word]:
                    for e in d[word][c]:
                        if rf in e:
                            print(word, d[word])
                            break;
                        else:
                            pass
                            # print("no related features for [", rf, "] is available")
            else:
                print(word, d[word])
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)
