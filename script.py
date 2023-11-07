# Read the data from the file
name = 'att48'
with open(f'dane/tsp-atsp/{name}.tsp', 'r') as file:
    lines = file.readlines()

# Extract the dimension from the relevant line
dimension = None
for line in lines:
    if line.startswith('DIMENSION'):
        dimension = int(line.split()[-1])
        break

# Check if the dimension is found
if dimension is None:
    raise ValueError("Dimension not found in the input file.")

# Extract the relevant data
data = []
start_reading = False
for line in lines:
    if line.startswith('EDGE_WEIGHT_SECTION'):
        start_reading = True
        continue
    if start_reading and line.strip() != 'EOF':
        row = line.split()
        data.extend(row)

# Convert the data to integers
data = [int(x) for x in data if x != 'EOF']

# Create the output
output = []
for i in range(dimension):
    row = data[i * dimension: (i + 1) * dimension]
    output.append(' '.join(map(str, row)))

# Write the output to a file
with open(f'dane/{name}.txt', 'w') as file:
    file.write('\n'.join(output))
