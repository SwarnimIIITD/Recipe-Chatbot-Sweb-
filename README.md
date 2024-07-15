## Competency questions:

1. What are ingredients for the particular recipe?
2. What are recipes along with instructions to make which have Total time to make less than given input time?
3. What are Recipe names that belong to a diet type?
4. Give some recipe names that belong to specific cuisine type.
5. Given number of serving to be done, give the Recipe name and instructions.
6. Have all the Recipe names that have given 2-3 names of product as their ingredient.
7. What is diet type of given Recipe name?
8. Which cuisine the given Recipe name belong to?
9. Having cuisine and course type give all the Recipe name that comes in that category.
10. Having diet and course type give all the Recipe name that comes in that category.
11. What is the URL for the Recipe having the Recipe name?

## SPARQL Queries used:

1.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT * WHERE {
        ?x ex:recipeName "Masala Karela Recipe" .
        ?x ex:ingredients ?ingred .
        ?x ex:instructions ?instruct .
        ?x schema:suitableForDiet ?diet .
        ?x schema:recipeCuisine ?cuisine .
        ?x schema:recipeCategory ?course .
        ?x schema:url ?url .
        ?x ex:takesTotalTime ?time .
        ?x ex:serves ?serv .
    }

2.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?name ?time WHERE {
        ?x ex:recipeName ?name .
        ?x ex:takesTotalTime ?time .
        FILTER (xsd:integer(?time) < 20)
    }

3.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:suitableForDiet "Vegetarian" .
    }

4.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:recipeCuisine "Thai" .
    }

5.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:recipeCategory "Side Dish" .
    }

6.

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x ex:serves "6" .
    }

7.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:recipeCuisine "Thai" .
        ?x schema:recipeCategory "Side Dish" .
    }

8.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:recipeCuisine "Thai" .
        ?x schema:suitableForDiet "Vegetarian".
    }

9.
    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name WHERE {
        ?x ex:recipeName ?name .
        ?x schema:recipeCategory "Side Dish" .
        ?x schema:suitableForDiet "Vegetarian".
    }

10.

    PREFIX ex: <http://example.org/>
    PREFIX schema: <http://schema.org/>

    SELECT ?name ?ing WHERE {
        ?x ex:recipeName ?name .
        ?x ex:ingredients ?ing .
        FILTER(REGEX(?ing, "water") && REGEX(?ing, "potato"))
    }