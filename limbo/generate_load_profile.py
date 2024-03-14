import argparse
import csv

def make_load_profile(begin, end, seconds, output):
    with open(output, "w") as f:
        writer = csv.writer(f)
        for i in range(seconds):
            writer.writerow([i, int((end - begin) * (i / seconds) + begin)])
        writer.writerow([seconds, end])

if __name__ == "__main__":
    # Make arg parser
    parser = argparse.ArgumentParser(description="Generate a load profile")
    parser.add_argument("-o", "--output", help="The file to write the load profile to")
    parser.add_argument("-b", "--begin", help="Number of requests to begin with")
    parser.add_argument("-e", "--end", help="Number of requests to end with")
    parser.add_argument("-s", "--seconds", help="Number of seconds to ramp up over")

    # Now ensure we have all required args
    args = parser.parse_args()
    if not args.output:
        parser.error("You must specify an output file")
    if not args.begin:
        parser.error("You must specify a begin value")
    if not args.end:
        parser.error("You must specify an end value")
    if not args.seconds:
        parser.error("You must specify a number of seconds")
        
    # Now make load profile
    make_load_profile(int(args.begin), int(args.end), int(args.seconds), args.output)