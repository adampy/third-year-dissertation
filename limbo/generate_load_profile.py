import argparse
import csv
import numpy as np

# Set numpy seed
np.random.seed(0)

def generate_default_filename(begin, end, seconds, constant, random):
    if constant:
        return f"lp_c{constant}_s{seconds}_r{random}.csv"
    else:
        return f"lp_b{begin}_e{end}_s{seconds}_r{random}.csv"

def apply_randomness(value, std_dev):
    # Apply randomness to value using normal distribution
    return round(value + (std_dev * np.random.randn()))

def make_load_profile_variable(begin, end, seconds, output, random=None):
    with open(output, "w") as f:
        writer = csv.writer(f)
        for i in range(seconds):
            base_requests = int((end - begin) * (i / seconds) + begin)
            if random is None:
                writer.writerow([i, base_requests])
            else:
                writer.writerow([i, apply_randomness(base_requests, random)])
        writer.writerow([seconds, end])
        
def make_load_profile_constant(constant, seconds, output, random=None):
    with open(output, "w") as f:
        writer = csv.writer(f)
        for i in range(seconds):
            if random is None:
                writer.writerow([i, constant])
            else:
                writer.writerow([i, apply_randomness(constant, random)])
        writer.writerow([seconds, constant])

if __name__ == "__main__":
    # Make arg parser
    parser = argparse.ArgumentParser(description="Generate a load profile")
    parser.add_argument("-o", "--output", help="The file to write the load profile to")
    parser.add_argument("-b", "--begin", help="Number of requests to begin with")
    parser.add_argument("-e", "--end", help="Number of requests to end with")
    parser.add_argument("-c", "--constant", help="Number of requests to keep constant")
    parser.add_argument("-s", "--seconds", help="Number of seconds to ramp up over")
    parser.add_argument("-r", "--random", help="Standard deviation to give to Gaussian sampling of number of requests")

    # Now ensure we have all required args
    args = parser.parse_args()        
    if not (args.begin and args.end) and not args.constant:
        parser.error("You must specify either a begin and end value or a constant value")
         
    if not args.seconds:
        parser.error("You must specify a number of seconds")
        
    if args.random and not args.random.isdigit():
        parser.error("Random must be an integer")
        
    # Cast all to ints
    begin = int(args.begin) if args.begin else None
    end = int(args.end) if args.end else None
    constant = int(args.constant) if args.constant else None
    seconds = int(args.seconds)
    random = int(args.random) if args.random else None
    output = generate_default_filename(begin, end, seconds, constant, random) if not args.output else args.output
        
    # Now make load profile
    if constant:
        make_load_profile_constant(constant, seconds, output, random)
    else:
        make_load_profile_variable(begin, end, seconds, output, random)