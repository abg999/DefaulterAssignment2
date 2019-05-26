from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from rest_framework.views import APIView
from dashboard_app import settings
import os
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessedImage
from django.core.files import File
from wordcloud import WordCloud, STOPWORDS


class GetAttributes(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            "detail": {
                "message": "Attributes Extracted",
                "attributes": settings.CSV_HEADS,
            }
        }, status=status.HTTP_201_CREATED)

class Scatter(APIView):

    def get(self, request, *args, **kwargs):
        if self.request.GET['parameter1'] and self.request.GET['parameter2']:
            dataset = pd.read_csv(settings.CSV_FILE_PATH, header=None, names=settings.CSV_HEADS)
            dataset = dataset.apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

            parameter1 = self.request.GET['parameter1']
            parameter2 = self.request.GET['parameter2']

            base_name = 'scatter_' + parameter1 + '_' + parameter2
            plt.figure(figsize=(8, 7))
            plt.scatter(dataset.loc[0:50, parameter1], dataset.loc[0:50, parameter2])
            plt.xlabel(parameter1)
            plt.ylabel(parameter2)
            plt.xticks(rotation=90)
            plt.title("Scatter plot for " + parameter1 + ' and ' + parameter2)

            file_path = os.path.join(settings.MEDIA_ROOT, base_name + '.png')
            print(file_path)
            plt.savefig(file_path)
            image_file = File(open(file_path, "rb"), name=(base_name + '.png'))

            process = ProcessedImage(image=image_file, name=base_name)
            ProcessedImage.save(process)

            return Response({
                "detail": {
                    "message": "Processing done.",
                    "image_url": process.image.url,
                }
            }, status=status.HTTP_201_CREATED)

class BarPlot(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.GET['parameter']:
            dataset = pd.read_csv(settings.CSV_FILE_PATH, header=None, names=settings.CSV_HEADS)
            dataset = dataset.apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

            parameter = self.request.GET['parameter']

            base_name = 'bar_plot_' + parameter
            plt.figure(figsize=(10, 11))
            locations = np.arange(len(dataset.loc[:, parameter].unique()))
            plt.bar(locations, dataset.loc[:, parameter].value_counts())
            plt.xticks(locations, dataset.loc[:, parameter].unique())
            plt.ylabel("Number of people")
            plt.xlabel(parameter)
            plt.xticks(rotation=90)
            plt.title("Bar plot for " + parameter)

            file_path = os.path.join(settings.MEDIA_ROOT, base_name + '.png')
            print(file_path)
            plt.savefig(file_path)
            image_file = File(open(file_path, "rb"), name=(base_name + '.png'))

            process = ProcessedImage(image=image_file, name=base_name)
            ProcessedImage.save(process)

            return Response({
                "detail": {
                    "message": "Processing done.",
                    "image_url": process.image.url,
                }
            }, status=status.HTTP_201_CREATED)

class PieChart(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.GET['parameter']:
            dataset = pd.read_csv(settings.CSV_FILE_PATH, header=None, names=settings.CSV_HEADS)
            dataset = dataset.apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

            parameter = self.request.GET['parameter']

            base_name = 'pie_chart_' + parameter
            plt.figure(figsize=(12, 5))
            plt.pie(dataset.loc[:, parameter].value_counts(), labels=dataset.loc[:, parameter].unique())
            plt.savefig(base_name)
            plt.title("Pie chart for " + parameter)

            file_path = os.path.join(settings.MEDIA_ROOT, base_name + '.png')
            plt.savefig(file_path)
            image_file = File(open(file_path, "rb"), name=(base_name + '.png'))

            process = ProcessedImage(image=image_file, name=base_name)
            ProcessedImage.save(process)

            return Response({
                "detail": {
                    "message": "Processing done.",
                    "image_url": process.image.url,
                }
            }, status=status.HTTP_201_CREATED)


class WordCloudAPI(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.GET['parameter']:
            dataset = pd.read_csv(settings.CSV_FILE_PATH, header=None, names=settings.CSV_HEADS)
            dataset = dataset.apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

            parameter = self.request.GET['parameter']

            dataset.loc[:, parameter].str = dataset.loc[:, parameter].str.replace(" ", "_")

            comment_words = ' '
            stopwords = set(STOPWORDS)

            # iterate through the csv file
            for val in dataset.loc[:, parameter]:

                # typecaste each val to string
                val = str(val)

                comment_words = comment_words + val + ' '


            wordcloud = WordCloud(width = 800, height = 800,
                            background_color ='white',
                            stopwords = stopwords,
                            min_font_size = 10).generate(comment_words)

            # plot the WordCloud image
            base_name = 'wordcloud_' + parameter
            file_path = os.path.join(settings.MEDIA_ROOT, base_name + '.png')

            plt.figure(figsize = (8, 8), facecolor = None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad = 0)
            plt.title("Word Cloud for " + parameter)
            plt.savefig(file_path)
            image_file = File(open(file_path, "rb"), name=(base_name + '.png'))

            process = ProcessedImage(image=image_file, name=base_name)
            ProcessedImage.save(process)

            return Response({
                "detail": {
                    "message": "Processing done.",
                    "image_url": process.image.url,
                }
            }, status=status.HTTP_201_CREATED)

class BoxPlot(APIView):
    def get(self, request, *args, **kwargs):
        dataset = pd.read_csv(settings.CSV_FILE_PATH, header=None, names=settings.CSV_HEADS)
        dataset = dataset.apply(lambda x: x.str.strip() if hasattr(x, 'str') else x)

        base_name = 'boxplot'
        file_path = os.path.join(settings.MEDIA_ROOT, base_name + '.png')

        dataset.drop(['fnlwgt'], axis=1)
        dataset.plot.box(grid='True')
        plt.figure(figsize=(12, 5))
        plt.savefig(file_path)
        image_file = File(open(file_path, "rb"), name=(base_name + '.png'))

        process = ProcessedImage(image=image_file, name=base_name)
        ProcessedImage.save(process)

        return Response({
            "detail": {
                "message": "Processing done.",
                "image_url": process.image.url,
            }
        }, status=status.HTTP_201_CREATED)