import plac

def main(excel_file_path: "Path to input training file.",
         excel_sheet_name: "Name of the excel sheet containing training data including columns 'Label' and 'Description'.",
         existing_model_path: "Path to an existing model to refine." = None,
         batch_size_start: "The smallest size of any minibatch." = 10.,
         batch_size_stop:  "The largest size of any minibatch." = 250.,
         batch_size_step:  "The step for increase in minibatch size." = 1.002,
         batch_test_steps: "Flag.  If True, show minibatch steps." = False): "Train a Spacy (http://spacy.io/) text classification model with gold document and label data until the model nears convergence (LOSS < 0.5)."


pass  # Implementation code goes here!


if __name__ == '__main__':
    import plac
    plac.call(main)
