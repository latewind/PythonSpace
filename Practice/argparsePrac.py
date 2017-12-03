import argparse
def run(args):
	print(str(args),'in run')
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-o','--on', action='store_true',
                    help='sum the integers (default: find the max)')

args = parser.parse_args(['-o',])
print(args)
if args.on :
	print("on")