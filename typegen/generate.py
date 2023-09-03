def save_text(file, text):
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
        f.close()
    return file

def generate_ordered_typed_dict(obj: dict, class_name: str = "RootTypedDict", output: str = None) -> str:
    if not isinstance(obj, dict):
        raise ValueError("Expected a dictionary as input.")

    pending_dicts = [(obj, class_name)]
    processed_dicts = {}
    output_lines = []

    while pending_dicts:
        current_dict, current_class_name = pending_dicts.pop(0)  # Use pop(0) to maintain order
        processed_dicts[str(current_dict)] = current_class_name

        class_definition = []
        class_definition.append(f"class {current_class_name}(TypedDict):\n")

        for key, value in current_dict.items():
            if isinstance(value, dict):
                if str(value) in processed_dicts:
                    nested_class_name = processed_dicts[str(value)]
                else:
                    nested_class_name = f"{key[0].upper()}{key[1:]}"
                    pending_dicts.append((value, nested_class_name))
                class_definition.append(f"    {key}: {nested_class_name}\n")
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    list_dict_name = f"{key[0].upper()}{key[1:]}List"
                    pending_dicts.append((value[0], list_dict_name))
                    class_definition.append(f"    {key}: List[{list_dict_name}]\n")
                else:
                    list_type = type(value[0]).__name__
                    class_definition.append(f"    {key}: List[{list_type}]\n")
            else:
                type_name = type(value).__name__
                class_definition.append(f"    {key}: {type_name}\n")

        class_definition.append("\n")
        output_lines = class_definition + output_lines  # Add new class definitions to the start

    # Prepending the import statement to the start of the generated code
    class_str = "from typing import TypedDict, List, Optional, Any\n\n" + ''.join(output_lines)
    class_str = class_str.replace('NoneType', 'Optional[Any]')
    file = ""
    
    if output:
        file = save_text(output, class_str)
    else:    
        file = save_text(f"out/{class_name}.py", class_str)
    return file, class_name