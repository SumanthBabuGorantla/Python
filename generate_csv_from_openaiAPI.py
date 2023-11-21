"""import openai
import csv
import time

# Set your OpenAI API key here
api_key = "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"

# Function to generate additional rows based on the input data
def generate_rows(input_csv, output_csv, num_rows=10,delay_seconds=21):
    with open(input_csv, 'r', newline='') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read and store the header row

        # Initialize the OpenAI API client
        openai.api_key = api_key

        # Read the existing 10 rows from the input CSV file
        input_data = [row for row in reader]
        #print(input_data)

        # Generate additional rows using the OpenAI API
        for _ in range(num_rows // 10):
            generated_data = []
            for row in input_data:
                #print(row)
                prompt = ','.join(row)
                columns =['s_no','name','age','country']

                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"generate csv rows similar to prompt given and s_no should be primary key: {prompt}",#prompt
                    max_tokens=10  # You can adjust this value based on your desired row length
                )
                generated_row = response.choices[0].text.strip()
                generated_data.append(generated_row.split(','))
                print(generated_data)

                time.sleep(delay_seconds)


            # Append the generated data to the input data
            #input_data.extend(generated_data)

    #Write the combined data to the output CSV file
    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(generated_data)#input_data

if __name__ == "__main__":
    input_csv = 'SampleCSVFile_2kb.csv'
    output_csv = 'output.csv'
    generate_rows(input_csv, output_csv)
    print(f"CSV file with 1000 rows generated: {output_csv}")"""




"""import openai
import csv
import time

# Set your OpenAI API key here
api_key = "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"

# Function to generate additional rows based on the input data with rate limiting
def generate_rows_with_rate_limit(input_csv, output_csv, num_rows=20, max_rows_per_request=5, delay_seconds=21):
    with open(input_csv, 'r', newline='') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read and store the header row

        # Initialize the OpenAI API client
        openai.api_key = api_key

        # Read the existing 10 rows from the input CSV file
        input_data = [row for row in reader]

        # Generate additional rows using the OpenAI API with rate limiting
        generated_data = []
        for _ in range(num_rows // max_rows_per_request):
            prompts = [','.join(row) for row in input_data[:max_rows_per_request]]
            responses = openai.Completion.create(
                engine="text-davinci-003",
                prompt=('\n'.join([f"Generate other CSV rows based on: {prompt}" for prompt in prompts])),
                max_tokens=30 * max_rows_per_request  # Adjust based on your desired row length
            )

            for response in responses.choices:
                generated_row = response.text.strip()
                print(generated_row)
                generated_data.append(generated_row.split(','))
                print(generated_data)

            # Introduce a delay to stay within rate limits
            if _ < (num_rows // max_rows_per_request) - 1:
                time.sleep(delay_seconds)

            # Remove the generated rows from input_data
            input_data = input_data[max_rows_per_request:]

        # Append the generated data to the input data
        input_data.extend(generated_data)

    # Write the combined data to the output CSV file
    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(input_data)

if __name__ == "__main__":
    input_csv = 'SampleCSVFile_2kb.csv'
    output_csv = 'output.csv'
    generate_rows_with_rate_limit(input_csv, output_csv)
    print(f"CSV file with 1000 rows generated: {output_csv}")
"""




import openai
import csv
import time


api_key = "your api key"


def generate_rows_with_batch(input_csv, output_csv, num_rows=100, batch_size=5, delay_seconds=21):
    with open(input_csv, 'r', newline='') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)


        openai.api_key = api_key


        input_data = [row for row in reader]

        generated_data = []

        for _ in range(num_rows // batch_size):
            prompts = [','.join(row) for row in input_data]
            batch_prompts = "\n".join(prompts)

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Generate many other unique CSV rows which are not in and based on:\n{batch_prompts}",
                max_tokens=30 * batch_size
            )

            generated_rows = response.choices[0].text.strip().split('\n')
            generated_data.extend([row.split(',') for row in generated_rows])
            print(generated_data)


            time.sleep(delay_seconds)


        input_data.extend(generated_data)


    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(input_data)

if __name__ == "__main__":
    input_csv = 'customer1.csv'
    output_csv = 'cust_modified'
    generate_rows_with_batch(input_csv, output_csv)
    print(f"CSV file with 1000 rows generated: {output_csv}")

