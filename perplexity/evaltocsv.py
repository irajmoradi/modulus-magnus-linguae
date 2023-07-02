import pandas as pd 
import matplotlib.pyplot as plt
import os

roman_to_decimal = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
    'XXI': 21,
    'XXII': 22,
    'XXIII': 23,
    'XXIV': 24,
    'XXV': 25,
    'XXVI': 26,
    'XXVII': 27,
    'XXVIII': 28,
    'XXIX': 29,
    'XXX': 30,
    'XXXI': 31,
    'XXXII': 32,
    'XXXIII': 33,
    'XXXIV': 34,
    'XXXV': 35
}

def create_pivot_table(df, index, columns, values): 
    df = df.groupby([index, columns])[values].mean().reset_index() 
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df
# ...

# iterate through all the files in results folder
directory = 'results'
data = []
for filename in os.listdir(directory):
    if filename.endswith(".raw.json"):
        continue
    filePath = os.path.join(directory, filename)
    if os.path.isfile(filePath):
        with open(filePath) as f:
            rate = f.read()
            try:
                accuracy = float(rate)
            except ValueError:
                print(f"Could not convert {rate} to float. In file: " + filename + " Skipping..")
                continue
        chapter, quiz_type, model = filename.split(".")[0:3]  # Adjusted according to the new file name structure
        data.append([model, chapter, quiz_type, accuracy])

# making data frame
df = pd.DataFrame(data, columns=["model", "chapter", "quiz_type", "accuracy"])
df['chapter'] = df['chapter'].str.split('_').str[1].map(roman_to_decimal)
print(df)

# ...


# pivoting to make specific tables
output_directory = "resultgraphs/"
# model chapter table
# No 'shot' column, so we remove that filter
filtered_df = df[df['model'].isin(['hugging', 'hugging13B', '13Bjuly2nd1'])] # Filter for specific models

pivot_df_model_chapter = create_pivot_table(filtered_df, 'model', 'chapter', 'accuracy')
pivot_df_model_chapter.to_csv(output_directory + 'results-model-chapter.csv')

# model chapter plot
pivot_df_model_chapter.T.plot(kind='line').set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter')
plt.legend(title='Model', loc='upper right')
plt.savefig(output_directory + 'model_chap.png')


# model chapter plot
pivot_df_model_chapter.T.plot(kind='line').set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter')
plt.legend(title='Model', loc='upper right')
plt.savefig(output_directory + 'model_chap.png')

# prompt quiz type table fixing ada
ada_df = df[df['model'] == 'hugging13B']

#pivot_df_style_quiztype = create_pivot_table(ada_df, 'style', 'quiz_type', 'accuracy')
#pivot_df_style_quiztype.to_csv(output_directory + 'results-style-quiz_type-ada.csv')

# question_type model table
#pivot_df_model_question_type = create_pivot_table(df, 'model', 'question_type', 'accuracy')
#pivot_df_model_question_type.to_csv(output_directory + 'results-model-questionType.csv')

# chapter quiz type table
pivot_df_chapter_quiztype = create_pivot_table(df, 'chapter', 'quiz_type', 'accuracy')
pivot_df_chapter_quiztype.to_csv(output_directory + 'results-chapter-quiz_type.csv')

# Group by model and calculate the mean accuracy
model_accuracy = df.groupby('model')['accuracy'].mean()
plt.clf()

# Create bar graph
model_accuracy.plot(kind='bar', xlabel='Model', ylabel='Accuracy', title='Accuracy per model')
plt.savefig(output_directory + 'model_accuracy.png')

#shot accuracy
#pivot_df_chapter_shot = create_pivot_table(df, 'model', 'shot', 'accuracy')
#pivot_df_chapter_shot.to_csv(output_directory + 'results-chapter-shot.csv')
#pivot_df_chapter_shot.T.plot(kind='bar').set(xlabel='chapter', ylabel='Accuracy', title='Accuracy per model and prompt style')
#plt.legend(title='Shot', loc='upper right')
#plt.savefig(output_directory + 'model_style1.png')

# prompt style accuracy
#pivot_df_model_style = create_pivot_table(df, 'model', 'style', 'accuracy')
#pivot_df_model_style.to_csv(output_directory + 'results-model-style.csv')

#pivot_df_model_style.T.plot(kind='bar').set(xlabel='Style', ylabel='Accuracy', title='Accuracy per model and prompt style')
#plt.legend(title='Model', loc='upper right')
#plt.savefig(output_directory + 'model_style.png')
