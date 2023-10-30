num_colors = 8


def generate_custom_colors(num_colors):
    # Define a list of color names
    color_names = [
        "#00f6ff",
        "#4cf0f5",
        "#69eaec",
        "#78e5e4",
        "#85e1dd",
        "#90dcd6",
        "#9ad8cf",
        "#a3d3c8",
        "#a8d0c4",
        "#adcdc0",
        "#b1cabb",
        "#b5c7b7",
        "#b9c4b3",
        "#bdc1ae",
        "#c1beaa",
        "#c4bba6",
        "#c7b8a1",
        "#cbb59d",
        "#cdb299",
        "#d0af94",
        "#d3ab90",
        "#d7a68a",
        "#dba183",
        "#de9c7c",
        "#e19776",
        "#e5906d",
        "#e88a66",
        "#eb835e",
        "#ef7b55",
        "#f2704a",
        "#f5653e",
        "#f85833",
        "#fa4a27",
        "#fc381a",
        "#fe1f0a",
    ]

    # Calculate the number of elements to be taken from the original list
    first_last = 1  # Number of elements to take from the start and end of the list
    middle_count = 30 - 2  # Number of elements excluding the first and last elements

    # Calculate the number of elements for the new list
    num_elements_new_list = first_last * 2 + min(middle_count, num_colors - 2)

    # Calculate the step size to evenly space the elements from the middle part of the list
    step = middle_count // (num_elements_new_list - first_last * 2)

    # Create a new list based on the criteria
    new_list = color_names[:first_last]  # Take the first element from the original list

    # Calculate elements for the middle part
    for i in range(first_last, num_elements_new_list - first_last):
        new_list.append(color_names[i * step])

    new_list += color_names[-first_last:]  # Take the last element from the original list

    print(new_list)

    return new_list

generate_custom_colors(num_colors)
