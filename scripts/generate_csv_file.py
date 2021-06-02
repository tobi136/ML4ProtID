import csv
from pyopenms import *

# Create a csv file with the three required columns as input for Prosit

# Load IdXML file generated by SimpleSearchEngineAlgorithm
protein_ids = []
peptide_ids = []

IdXMLFile().load("SSE_results.idXML", protein_ids, peptide_ids)

# Set the collision energy
collision_energy = 27

# Specify the header
header = ['modified_sequence', 'collision_energy', 'precursor_charge']

# Write the csv file serving as input for Prosit
with open('prosit_input_test.csv', 'w') as f:
    writer = csv.writer(f)

    # Write the header
    writer.writerow(header)

    # Initialize array containing rows
    # -> Not necessary if no filtering is needed
    # rows = []

    # Iterate over the hits and write the rows containing the respective values
    for p in peptide_ids:
        for h in p.getHits():
            sequence = str(h.getSequence())

            # Adjust needed notation for oxidation (other modifications are not supported)
            sequence = sequence.replace("Oxidation", "ox")

            # Remove (Carbamidomethyl) notation after cysteins, since each C is treated as C with carbamidomethylation
            sequence = sequence.replace("(Carbamidomethyl)", "")

            # Skip sequences exceeding the limit of 30 amino acids (prevent Prosit error)
            if len(sequence) > 30:
                continue

            row = [sequence, collision_energy, h.getCharge()]

            # Avoid redundancy: Only append if row not already given
            # -> Omit this filtering in order to keep the respective order to allow the correct assignment of the
            # intensities
            #if row not in rows:
            #    rows.append(row)

            # Write respective row to csv file
            writer.writerow(row)

    # Write rows to csv file
    # for r in rows:
    #    writer.writerow(r)
