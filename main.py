import math
import os
from rdflib import Graph

# run python3 main.py

def executeQuery(file_path, query, type, labels):
    # Load the RDF graph from the .ttl file
    graph = Graph()
    graph.parse(file_path, format='ttl')

    # Define RDF prefixes
    prefixes = dict(graph.namespaces())

    # Execute the query and print results
    results = graph.query(query, initNs=prefixes)
    if (len(results) == 0):
        print("No results found!!")
    else:
        if (len(labels) == 0):
            for row in results:
                print(row[0])
        else:
            i = 0
            for row in results:
                formatted_row = [f"{labels[i]}: {value.n3() if hasattr(value, 'n3') else value}" for i, value in enumerate(row)]
                if (type == "details" or type == "suggestions"):
                    print("\n\n".join(formatted_row))
                else:
                    print("\n".join(formatted_row))
                if (i != len(results) - 1):
                    print()
                i += 1
    
    if (type == ""):
        print()
        print("-------------------||-------------------------------------||-------------------")
        print()
        print("Menu")
        print()
        print("   1. Get all details of a particular recipe")
        print()
        print("   2. Go Back")
        print()
        print("   3. Exit")
        print()
        option = int(input("Enter option : "))
        print()
        if (option == 1):
            print("-------------------||-------------------------------------||-------------------")
            print()
            name = input("Enter recipe name : ")
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?ingred ?instruct ?diet ?cuisine ?course ?url ?time ?serv WHERE {{
                    ?x ex:recipeName ?name .
                    ?x ex:ingredients ?ingred .
                    ?x ex:instructions ?instruct .
                    ?x schema:suitableForDiet ?diet .
                    ?x schema:recipeCuisine ?cuisine .
                    ?x schema:recipeCategory ?course .
                    ?x schema:url ?url .
                    ?x ex:takesTotalTime ?time .
                    ?x ex:serves ?serv .
                    FILTER (regex(?name, "{name}", "i"))
                }}
            """
            labels = ['ingredients', 'instructions', 'suitableForDiet', 'recipeCuisine', 'recipeCategory', 'url', 'takesTotalTime', 'serves']
            print()
            executeQuery(file_path, query, "details", labels)

        elif (option == 2):
            main(file_path)
        
        else:
            print("-------------------||-------------------------------------||-------------------")
            print("-------------------||------------- THANK YOU -------------||-------------------")
            print("-------------------||-------------------------------------||-------------------")
            exit()
    
    elif (type == "suggestions"):
        data = []
        for row in results:
            formatted_row = [f"{value.n3() if hasattr(value, 'n3') else value}" for i, value in enumerate(row)]
            for i in range(len(formatted_row)):
                if (i != 0 and i != 1 and i != 5):
                    data.append(formatted_row[i])
        print()
        print("-------------------||-------------------------------------||-------------------")
        print()
        print("Menu")
        print()
        print("   1. Get all recipes of same diet")
        print()
        print("   2. Get all recipes of same cuisine")
        print()
        print("   3. Get all recipes of same course")
        print()
        print("   4. Get all recipes that take same time")
        print()
        print("   5. Get all recipes of same number of servings")
        print()
        print("   6. Go Back")
        print()
        print("   7. Exit")
        print()
        option = int(input("Enter option : "))
        print()
        print("-------------------||-------------------------------------||-------------------")
        if (option == 1):
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?name WHERE {{
                    ?x ex:recipeName ?name .
                    ?x schema:suitableForDiet {data[0]} .
                }}
            """
            print()
            executeQuery(file_path, query, "", [])
            print()

        elif (option == 2):
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?name WHERE {{
                    ?x ex:recipeName ?name .
                    ?x schema:recipeCuisine {data[1]} .
                }}
            """
            print()
            executeQuery(file_path, query, "", [])
            print()

        elif (option == 3):
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?name WHERE {{
                    ?x ex:recipeName ?name .
                    ?x schema:recipeCategory {data[2]} .
                }}
            """
            print()
            executeQuery(file_path, query, "", [])
            print()

        elif (option == 4):
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?name WHERE {{
                    ?x ex:recipeName ?name .
                    ?x ex:takesTotalTime {data[3]} .
                }}
            """
            print()
            executeQuery(file_path, query, "", [])
            print()

        elif (option == 5):
            query = f"""
                PREFIX ex: <http://example.org/>
                PREFIX schema: <http://schema.org/>

                SELECT ?name WHERE {{
                    ?x ex:recipeName ?name .
                    ?x ex:serves {data[4]} .
                }}
            """
            print()
            executeQuery(file_path, query, "", [])
            print()

        elif (option == 6):
            main(file_path)

        else:
            print("-------------------||-------------------------------------||-------------------")
            print("-------------------||------------- THANK YOU -------------||-------------------")
            print("-------------------||-------------------------------------||-------------------")
            exit()

def listIngredientsWithServings(file_path, name, serves):
    # Load the RDF graph from the .ttl file
    graph = Graph()
    graph.parse(file_path, format='ttl')

    # Define RDF prefixes
    prefixes = dict(graph.namespaces())

    query = f"""
        PREFIX ex: <http://example.org/>
        PREFIX schema: <http://schema.org/>

        SELECT ?ingred WHERE {{
            ?x ex:recipeName ?name .
            ?x ex:ingredients ?ingred .
            FILTER (regex(?name, "{name}", "i"))
        }}
    """

    # Execute the query and print results
    results = graph.query(query, initNs=prefixes)
    ingred = []

    query = f"""
        PREFIX ex: <http://example.org/>
        PREFIX schema: <http://schema.org/>

        SELECT ?serves WHERE {{
            ?x ex:recipeName ?name .
            ?x ex:serves ?serves .
            FILTER (regex(?name, "{name}", "i"))
        }}
    """

    # Execute the query and print results
    serving = graph.query(query, initNs=prefixes)
    given = 0

    for row in serving:
        formatted_row = [f"{value.n3() if hasattr(value, 'n3') else value}" for i, value in enumerate(row)]
        formatted_row[0] = formatted_row[0][1:]
        formatted_row[0] = formatted_row[0][:len(formatted_row) - 2]
        given += int(formatted_row[0])

    if (len(results) == 0):
        print("No results found!!")
        return
    else:
        for row in results:
            formatted_row = [f"{value.n3() if hasattr(value, 'n3') else value}" for i, value in enumerate(row)]
            formatted_row[0] = formatted_row[0][1:]
            formatted_row[0] = formatted_row[0][:len(formatted_row) - 2]
            ingred = formatted_row[0].split(",")
        for i in ingred:
            print(multiply_numbers_in_string(i, serves, given))

def multiply_numbers_in_string(string, k, given):
    # Helper function to multiply numbers in a string by k
    words = string.split()
    for i, word in enumerate(words):
        if word.isdigit():
            words[i] = str(math.ceil(int(word) * k/given))
    return ' '.join(words)

def main(file_path):
    print("-------------------||-------------------------------------||-------------------")
    print()
    print("Main menu")
    print()
    print("   1. List all recipes")
    print()
    print("   2. Get all details of a particular recipe")
    print()
    print("   3. Get all recipes which take time less than x minutes")
    print()
    print("   4. Get all recipes based on a particular diet")
    print()
    print("   5. Get all recipes based on a particular cuisine")
    print()
    print("   6. Get all recipes based on a particular course")
    print()
    print("   7. Get all recipes based on x number of servings")
    print()
    print("   8. Get all recipes based on a particular cuisine and course")
    print()
    print("   9. Get all recipes based on a particular cuisine and diet")
    print()
    print("   10. Get all recipes based on a particular course and diet")
    print()
    print("   11. Get all recipes based on particular ingredients")
    print()
    print("   12. List all diets")
    print()
    print("   13. List all cuisines")
    print()
    print("   14. List all courses")
    print()
    print("   15. Get all ingredients of a recipe based on x number of servings")
    print()
    print("   16. Exit")
    print()
    option = int(input("Enter option : "))
    print()

    if (option == 1):
        print("-------------------||-------------------------------------||-------------------")
        print()
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name ?diet ?cuisine ?course ?time ?serv WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:suitableForDiet ?diet .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:recipeCategory ?course .
                ?x ex:takesTotalTime ?time .
                ?x ex:serves ?serv .
            }}
        """
        labels = ['Recipe Name', 'Diet', 'Cuisine', 'Course', 'Total Time', 'Serves']
        print()
        executeQuery(file_path, query, "", labels)
        print()

    elif (option == 2):
        print("-------------------||-------------------------------------||-------------------")
        print()
        name = input("Enter recipe name : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?ingred ?instruct ?diet ?cuisine ?course ?url ?time ?serv WHERE {{
                ?x ex:recipeName ?name .
                ?x ex:ingredients ?ingred .
                ?x ex:instructions ?instruct .
                ?x schema:suitableForDiet ?diet .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:recipeCategory ?course .
                ?x schema:url ?url .
                ?x ex:takesTotalTime ?time .
                ?x ex:serves ?serv .
                FILTER (regex(?name, "{name}", "i"))
            }}
        """
        labels = ['Ingredients', 'Instructions', 'Diet', 'Cuisine', 'Course', 'URL', 'Total Time', 'Serves']
        print()
        executeQuery(file_path, query, "suggestions", labels)
        print()

    elif (option == 3):
        print("-------------------||-------------------------------------||-------------------")
        print()
        time = input("Enter time x : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?name ?time WHERE {{
                ?x ex:recipeName ?name .
                ?x ex:takesTotalTime ?time .
                FILTER (xsd:integer(?time) < {time})
            }}
        """
        labels = ['Recipe Name', 'Total time taken']
        print()
        executeQuery(file_path, query, "", labels)
        print()

    elif (option == 4):
        print("-------------------||-------------------------------------||-------------------")
        print()
        diet = input("Enter diet type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:suitableForDiet ?diet .
                FILTER(REGEX(?diet, "^{diet}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "", [])
        print()

    elif (option == 5):
        print("-------------------||-------------------------------------||-------------------")
        print()
        cuisine = input("Enter cuisine type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCuisine ?cuisine .
                FILTER(REGEX(?cuisine, "^{cuisine}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "", [])
        print()

    elif (option == 6):
        print("-------------------||-------------------------------------||-------------------")
        print()
        course = input("Enter course type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCategory ?course .
                FILTER(REGEX(?course, "^{course}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "", [])
        print()

    elif (option == 7):
        print("-------------------||-------------------------------------||-------------------")
        print()
        serves = input("Enter servings x : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x ex:serves "{serves}" .
            }}
        """
        print()
        executeQuery(file_path, query, "", [])
        print()

    elif (option == 8):
        print("-------------------||-------------------------------------||-------------------")
        print()
        cuisine = input("Enter cuisine type : ")
        print()
        course = input("Enter course type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:recipeCategory ?course .
                FILTER(REGEX(?cuisine, "^{cuisine}$", "i") && REGEX(?course, "^{course}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "details", [])
        print()
        suggQuery = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:recipeCategory ?course .
                FILTER((REGEX(?cuisine, "^{cuisine}$", "i") && !REGEX(?course, "^{course}$", "i")) ||
                    (!REGEX(?cuisine, "^{cuisine}$", "i") && REGEX(?course, "^{course}$", "i")))
            }}
        """
        print("---------------||----- Some suggestions for you: -----||-------------------")
        print()
        executeQuery(file_path, suggQuery, "", [])
        print()

    elif (option == 9):
        print("-------------------||-------------------------------------||-------------------")
        print()
        cuisine = input("Enter cuisine type : ")
        print()
        diet = input("Enter diet type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:suitableForDiet ?diet .
                FILTER(REGEX(?cuisine, "^{cuisine}$", "i") && REGEX(?diet, "^{diet}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "details", [])
        print()
        suggQuery = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCuisine ?cuisine .
                ?x schema:suitableForDiet ?diet .
                FILTER((REGEX(?cuisine, "^{cuisine}$", "i") && !REGEX(?diet, "^{diet}$", "i")) ||
                    (!REGEX(?cuisine, "^{cuisine}$", "i") && REGEX(?diet, "^{diet}$", "i")))
            }}
        """
        print("-------------------||----- Some suggestions for you: -----||-------------------")
        print()
        executeQuery(file_path, suggQuery, "", [])
        print()

    elif (option == 10):
        print("-------------------||-------------------------------------||-------------------")
        print()
        course = input("Enter course type : ")
        print()
        diet = input("Enter diet type : ")
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCategory ?course .
                ?x schema:suitableForDiet ?diet .
                FILTER(REGEX(?course, "^{course}$", "i") && REGEX(?diet, "^{diet}$", "i"))
            }}
        """
        print()
        executeQuery(file_path, query, "details", [])
        print()
        suggQuery = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name WHERE {{
                ?x ex:recipeName ?name .
                ?x schema:recipeCategory ?course .
                ?x schema:suitableForDiet ?diet .
                FILTER((REGEX(?course, "^{course}$", "i") && !REGEX(?diet, "^{diet}$", "i")) ||
                    (!REGEX(?course, "^{course}$", "i") && REGEX(?diet, "^{diet}$", "i")))
            }}
        """
        print("-------------------||----- Some suggestions for you: -----||-------------------")
        print()
        executeQuery(file_path, suggQuery, "", [])
        print()

    elif (option == 11):
        print("-------------------||-------------------------------------||-------------------")
        print()
        ingredList = input("Enter ingredients : ").split(' ')
        filter_condition = " && ".join([f'REGEX(?ing, "{ing}")' for ing in ingredList])
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT ?name ?ing WHERE {{
                ?x ex:recipeName ?name .
                ?x ex:ingredients ?ing .
                FILTER({filter_condition})
            }}
        """
        labels = ['Recipe Name', 'Ingredients']
        print()
        executeQuery(file_path, query, "", labels)
        print()

    elif (option == 12):
        print("-------------------||-------------------------------------||-------------------")
        print()
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT DISTINCT ?diet WHERE {{
                ?x schema:suitableForDiet ?diet .
            }}
        """
        executeQuery(file_path, query, "details", [])
        print()

    elif (option == 13):
        print("-------------------||-------------------------------------||-------------------")
        print()
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT DISTINCT ?cuisine WHERE {{
                ?x schema:recipeCuisine ?cuisine .
            }}
        """
        executeQuery(file_path, query, "details", [])
        print()

    elif (option == 14):
        print("-------------------||-------------------------------------||-------------------")
        print()
        query = f"""
            PREFIX ex: <http://example.org/>
            PREFIX schema: <http://schema.org/>

            SELECT DISTINCT ?course WHERE {{
                ?x schema:recipeCategory ?course .
            }}
        """
        executeQuery(file_path, query, "details", [])
        print()

    elif (option == 15):
        print("-------------------||-------------------------------------||-------------------")
        print()
        name = input("Enter recipe name : ")
        print()
        serves = int(input("Enter servings x : "))
        print()
        listIngredientsWithServings(file_path, name, serves)
        print()

    else:
        print("-------------------||-------------------------------------||-------------------")
        print("-------------------||------------- THANK YOU -------------||-------------------")
        print("-------------------||-------------------------------------||-------------------")
        exit()

if __name__ == "__main__":
    file_path = "triples.ttl"
    os.system('cls')
    print("-------------------||-------------------------------------||-------------------")
    print("-------------------||-- WELCOME TO THE WORLD OF RECIPES --||-------------------")
    while True:
        main(file_path)