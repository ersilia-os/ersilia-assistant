from typing import List, Generator
import re

class RecipeGenerator:
    def __init__(self) -> None:
        self.fetch_cmd = "ersilia fetch eos-identifier"
        self.serve_cmd = "ersilia serve eos-identifier"
        self.run_cmd = "ersilia run -i input.csv -o output_eos-identifier.csv"
        self.close_cmd = "ersilia close"
        self.init_string = """Use the following recipe to run the identified models on your data. The following instructions assume that your dataset is stored in a file called 'input.csv'.
        \nThis file should contain a column called smiles with the SMILES strings of the molecules in your dataset.\n
        """

    def get_models(self, text: str) -> List[str]:
        """A parser to extract model identifiers from a given text

        Parameters
        ----------
        text : The Generated text from which to extract the models
            _description_

        Returns
        -------
        List[str]
            List of model identifiers
        """
        return set(re.findall(r"eos[a-zA-Z0-9]+", text))
    
    def generate(self, text: str) -> Generator[str, None, None]:
        models = self.get_models(text)

        final_recipe = self.init_string
        for mdl in models:
            single_model_recipe = "\n```bash\n"
            single_model_recipe += self.fetch_cmd.replace("eos-identifier", mdl) + "\n"
            single_model_recipe += self.serve_cmd.replace("eos-identifier", mdl) + "\n"
            single_model_recipe += self.run_cmd.replace("eos-identifier", mdl) + "\n"
        
            final_recipe += single_model_recipe + "```\n"
            
        for token in final_recipe.split(sep=" "):
            yield token+" "
        
