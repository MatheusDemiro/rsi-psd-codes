from RandomForestClassifier import RandomForest

rf_instance = RandomForest()

data = rf_instance.generateData()

trainingData, testData = data.randomSplit([0.7, 0.3])

randomForestModel = rf_instance.randomForestClassifier(data, trainingData)

predictions = randomForestModel.transform(testData)

predictions.select("predictedLabel", "classe", "features").show(95, False)

print(rf_instance.getError(predictions))