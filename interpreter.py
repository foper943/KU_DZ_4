import struct
import yaml

def interpret(binary_file, result_file):
    memory = [0] * 1024  # Пример памяти
    result = {}
    
    with open(binary_file, 'rb') as f:
        while byte := f.read(8):  # Чтение 8 байт за раз
            A, B, C = struct.unpack('>3I', byte)
            
            if A == 1:
                memory[B] = C
            elif A == 12:
                memory[C] = memory[B]
            elif A == 15:
                memory[B + C] = memory[D]
            elif A == 13:
                memory[C] = abs(memory[B])
    
    # Сохранение результатов в YAML
    with open(result_file, 'w') as f:
        yaml.dump(result, f)

# Пример использования
interpret("program.bin", "result.yaml")
