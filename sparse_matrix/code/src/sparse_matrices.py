#!/usr/bin/python3
class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}  # to Store non-zero elements as {(row, col): value}.

        if matrixFilePath:
            self.load_matrix(matrixFilePath)

    def load_matrix(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.numRows = int(lines[0].split('=')[1])
                self.numCols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    if line.strip():
                        entry = line.strip().strip('()').split(',')
                        row, col, value = int(entry[0]), int(entry[1]), int(entry[2])
                        self.elements[(row, col)] = value
        except (ValueError, IndexError):
            raise ValueError("Input file has wrong format")

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def __str__(self):
        result = []
        for (row, col), value in self.elements.items():
            result.append(f"({row}, {col}, {value})")
        return "\n".join(result)


def subtractionOfSparseMatrices(sparseMatrixOne, sparseMatrixTwo):
    if sparseMatrixOne.numRows != sparseMatrixTwo.numRows or sparseMatrixOne.numCols != sparseMatrixTwo.numCols:
        raise ValueError("Matrix dimensions do not match for subtraction")

    result = SparseMatrix(numRows=sparseMatrixOne.numRows, numCols=sparseMatrixOne.numCols)

    all_keys = set(sparseMatrixOne.elements.keys()).union(sparseMatrixTwo.elements.keys())
    for key in all_keys:
        diff_value = sparseMatrixOne.get_element(*key) - sparseMatrixTwo.get_element(*key)
        result.set_element(key[0], key[1], diff_value)

    return result

def MultiplicationOfMatrices(sparseMatrixOne, sparseMatrixTwo):
    if sparseMatrixOne.numCols != sparseMatrixTwo.numRows:
        raise ValueError("Matrix dimensions do not match for multiplication")

    result = SparseMatrix(numRows=sparseMatrixOne.numRows, numCols=sparseMatrixTwo.numCols)

    for (i, k), value1 in sparseMatrixOne.elements.items():
        for j in range(sparseMatrixTwo.numCols):
            value2 = sparseMatrixTwo.get_element(k, j)
            if value2 != 0:
                current_value = result.get_element(i, j)
                result.set_element(i, j, current_value + value1 * value2)

    return result

def additionOfMatrices(sparseMatrixOne, sparseMatrixTwo):
    if sparseMatrixOne.numRows != sparseMatrixTwo.numRows or sparseMatrixOne.numCols != sparseMatrixTwo.numCols:
        raise ValueError("Matrix dimensions do not match for addition")

    result = SparseMatrix(numRows=sparseMatrixOne.numRows, numCols=sparseMatrixOne.numCols)

    all_keys = set(sparseMatrixOne.elements.keys()).union(sparseMatrixTwo.elements.keys())
    for key in all_keys:
        sum_value = sparseMatrixOne.get_element(*key) + sparseMatrixTwo.get_element(*key)
        result.set_element(key[0], key[1], sum_value)

    return result

def main():
    try:
        # Hardcoded file paths for the matrix files
        matrixOnePath = r"../../sample_inputs/easy_sample_03_1.txt"  # my actual path
        matrixTwoPath = r"../../sample_inputs/easy_sample_03_2.txt"  # actual path

        sparseMatrixOne = SparseMatrix(matrixOnePath)
        sparseMatrixTwo = SparseMatrix(matrixTwoPath)

        print("Select one of the operations by typing either 1, 2, or 3: \n1) Add  2) Subtract  3) Multiply")
        choice = input().strip()

        if choice == '1':
            result = additionOfMatrices(sparseMatrixOne, sparseMatrixTwo)
        elif choice == '2':
            result = subtractionOfSparseMatrices(sparseMatrixOne, sparseMatrixTwo)
        elif choice == '3':
            result = MultiplicationOfMatrices(sparseMatrixOne, sparseMatrixTwo)
        else:
            print("Invalid choice")
            return

        print("Result:")
        print(result)

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: The File is not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
