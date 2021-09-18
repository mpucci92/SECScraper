from FullFilePath import createFullPath,createFullPathSolo
from RiskFactors import riskFactors,riskFactorDataframe,files,text,date
from TextEmbeddings import transformerModel
from SECDownloader import downloadSEC
import sklearn

if __name__ == '__main__':
    #ticker_to_download = 'ZM'
    path_to_save = r"C:\Users\mp094\Desktop\SEC_Financial_documents"
    path_to_model = r"C:\Users\mp094\Desktop\BERT_BASE_NER\distilbert-base-nli-stsb-mean-tokens"
    article_type = '10-Q'
    numberArticles = 1
    ticker = 'AMZN'

    #downloadSEC(article_type,ticker_to_download,path_to_save,numberArticles)

    #full_file_path = createFullPathSolo(ticker)
    full_file_path = createFullPath(['BA','ZM','AMZN','UBER','TSLA','SPCE'])
    riskFactors(full_file_path)
    df = riskFactorDataframe(files, text, date)

    temp = df[(df['tickers'] == ticker) & (df['article_type'] == article_type)].sort_values(
        by='timestamp').reset_index(drop=True)

    cosineScores = []

    for i in range(len(temp)):
        try:
            text1 = [temp.text.iloc[i]]
            text2 = [temp.text.iloc[i + 1]]

            embedding1 = transformerModel(text1, path_to_model, 256)
            embedding2 = transformerModel(text2, path_to_model, 256)

            cosine_similarity_score = sklearn.metrics.pairwise.cosine_similarity(embedding1, embedding2, dense_output=True)[0][0]
            cosineScores.append(cosine_similarity_score)
        except Exception as e:
            cosine_similarity_score = None
            cosineScores.append(cosine_similarity_score)

    temp['cosineScores'] = cosineScores

    print(temp['cosineScores'])
    #print(temp.text.iloc[0][0:1000])
    #print(full_file_path)
    #print(embedding1)
