import os

def remove_last_two_lines_from_all(folder_path): #Проверка сущевствования файла
    if not os.path.exists(folder_path):
        print("Указанная папка не найдена.")
        return


    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
                new_lines = lines[:-2] if len(lines) > 2 else []
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)
                    
                print(f"Файл {file_name} успешно обработан.")
                
            except Exception as e:
                print(f"Не удалось обработать {file_name}: {e}")

folder = '.' 
remove_last_two_lines_from_all(folder)
