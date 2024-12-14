import struct
import yaml


def assemble(input_file, output_bin, log_file):
    # Чтение исходного файла
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_program = []  # Список бинарных команд
    log_data = {}  # Словарь для логирования

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()

        # Обработка команды LOAD_CONSTANT (Загрузка константы)
        if parts[0] == "LOAD_CONSTANT":
            A, B, C = map(int, parts[1:])
            # Преобразование C в абсолютное значение (если это необходимо)
            C = abs(C)  # Преобразование в абсолютное значение для обеспечения положительности

            # Проверка, чтобы значения A, B и C не выходили за пределы
            if not (0 <= A <= 15):
                raise ValueError(f"Invalid value for A: {A}")
            if not (0 <= B <= (2**28 - 1)):
                raise ValueError(f"Invalid value for B: {B}")
            if not (0 <= C <= (2**30 - 1)):
                raise ValueError(f"Invalid value for C: {C}")

            # Формирование команды: A (4 бита), B (28 бит), C (30 бит)
            command = struct.pack('>I', (A << 28) | (B << 4) | (C & 0xF))
            binary_program.append(command)
            log_data[f"LOAD_CONSTANT_{len(binary_program)}"] = {"A": A, "B": B, "C": C}

        # Обработка команды READ_MEMORY (Чтение из памяти)
        elif parts[0] == "READ_MEMORY":
            A, B, C = map(int, parts[1:])
            # Преобразование C в абсолютное значение (если это необходимо)
            C = abs(C)

            # Проверка, чтобы значения A, B и C не выходили за пределы
            if not (0 <= A <= 15):
                raise ValueError(f"Invalid value for A: {A}")
            if not (0 <= B <= (2**28 - 1)):
                raise ValueError(f"Invalid value for B: {B}")
            if not (0 <= C <= (2**28 - 1)):
                raise ValueError(f"Invalid value for C: {C}")

            # Формирование команды: A (4 бита), B (28 бит), C (28 бит)
            command = struct.pack('>I', (A << 28) | (B << 4) | (C & 0xF))
            binary_program.append(command)
            log_data[f"READ_MEMORY_{len(binary_program)}"] = {"A": A, "B": B, "C": C}

        # Обработка команды WRITE_MEMORY (Запись в память)
        elif parts[0] == "WRITE_MEMORY":
            A, B, C, D = map(int, parts[1:])
            # Преобразование C и D в абсолютное значение (если это необходимо)
            C = abs(C)
            D = abs(D)

            # Проверка, чтобы значения A, B, C и D не выходили за пределы
            if not (0 <= A <= 15):
                raise ValueError(f"Invalid value for A: {A}")
            if not (0 <= B <= (2**28 - 1)):
                raise ValueError(f"Invalid value for B: {B}")
            if not (0 <= C <= (2**30 - 1)):
                raise ValueError(f"Invalid value for C: {C}")
            if not (0 <= D <= (2**28 - 1)):
                raise ValueError(f"Invalid value for D: {D}")

            # Формирование команды: A (4 бита), B (28 бит), C (30 бит), D (28 бит)
            command = struct.pack('>I', (A << 28) | (B << 4) | (C & 0xF) | (D & 0xF))
            binary_program.append(command)
            log_data[f"WRITE_MEMORY_{len(binary_program)}"] = {"A": A, "B": B, "C": C, "D": D}

        # Обработка команды ABSOLUTE (Абсолютное значение)
        elif parts[0] == "ABSOLUTE":
            A, B, C = map(int, parts[1:])
            # Преобразование C в абсолютное значение (если это необходимо)
            C = abs(C)

            # Проверка, чтобы значения A, B и C не выходили за пределы
            if not (0 <= A <= 15):
                raise ValueError(f"Invalid value for A: {A}")
            if not (0 <= B <= (2**28 - 1)):
                raise ValueError(f"Invalid value for B: {B}")
            if not (0 <= C <= (2**30 - 1)):
                raise ValueError(f"Invalid value for C: {C}")

            # Формирование команды: A (4 бита), B (28 бит), C (30 бит)
            command = struct.pack('>I', (A << 28) | (B << 4) | (C & 0xF))
            binary_program.append(command)
            log_data[f"ABSOLUTE_{len(binary_program)}"] = {"A": A, "B": B, "C": C}

        else:
            print(f"Unknown command: {line}")

    # Запись бинарного файла
    with open(output_bin, 'wb') as f:
        for command in binary_program:
            f.write(command)

    # Запись лога в YAML
    with open(log_file, 'w') as f:
        yaml.dump(log_data, f, default_flow_style=False)


# Пример использования
if __name__ == "__main__":
    input_file = "program.asm"
    output_bin = "program.bin"
    log_file = "program_log.yaml"
    assemble(input_file, output_bin, log_file)
