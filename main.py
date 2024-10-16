from hyperon import MeTTa, SymbolAtom, ExpressionAtom, GroundedAtom
import os
import glob

# Initialize MeTTa and create a new space
metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    """Load .metta files from the dataset into the MeTTa grounding space."""
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f"!(load-ascii &space {path})")
            print(f"Successfully loaded dataset from '{path}'.")
            # Print the current content of the space after loading each file
            print(f"Current space content after loading '{path}':")
            print(metta.run("!(show-space &space)"))
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    
    print(f"Finished loading {len(paths)} datasets.")

try:
    # Load the dataset from the specified path
    load_dataset("./Data")
except Exception as e:
    print(f"An error occurred: {e}")
result = metta.run('!(find &space (transcribed_to (gene ENSG00000175793) $transcript))')
print(result)

# Get transcript for a gene
def get_transcript(gene):
    """Query the space for transcripts related to a given gene."""
    gene_id = gene[0]  # Extracting gene id from input
    result = metta.run(f'''
    !(find &space (transcribed_to {gene_id} $transcript))
    ''')
    return result

# Get protein for a gene
def get_protein(gene):
    """Query the space for proteins related to transcripts of a given gene."""
    gene_id = gene[0]  # Extracting gene id from input
    result = metta.run(f'''
    !(find &space (translates_to $transcript $protein))
    ''')
    return result

# Serializer for MeTTa result
def metta_serializer(metta_result):
    """Parse and serialize the results from MeTTa queries."""
    parsed_result = []
    for res in metta_result:
        if isinstance(res, list):  # Assuming result is a list of statements
            for statement in res:
                if isinstance(statement, list):  # Assuming each result is a list of tuples
                    _, edge_data = statement  # Extracting the edge data
                    if len(edge_data) == 3:  # Ensure it matches expected length
                        edge_type, source, target = edge_data
                        if edge_type == 'transcribed_to':
                            parsed_result.append({
                                'edge': 'transcribed_to',
                                'source': source,  # gene
                                'target': target   # transcript
                            })
                        elif edge_type == 'translates_to':
                            parsed_result.append({
                                'edge': 'translates_to',
                                'source': source,  # transcript
                                'target': target   # protein
                            })
    return parsed_result

# Example usage
try:
    # Load the dataset from the specified path
    load_dataset("./Data")
except Exception as e:
    print(f"An error occurred: {e}")

# 1. Fetch transcripts
transcript_result = get_transcript(['gene ENSG00000166913'])
print(f"Transcript Result: {transcript_result}")

# 2. Fetch proteins
protein_result = get_protein(['gene ENSG00000166913'])
print(f"Protein Result: {protein_result}")

# 3. Serialize the transcript result
parsed_result = metta_serializer(transcript_result)
print(f"Parsed Transcript Result: {parsed_result}")
