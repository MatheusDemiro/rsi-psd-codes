from RandomForestClassifier import RandomForest

def getError():
    accuracy = rf_instance.getAcurrancy(predictions)

    return "Test Accuracy Rate: %g\nTest Error Rate: %g" % (accuracy, 1.0 - accuracy)

rf_instance = RandomForest()

data = rf_instance.generateData()

trainingData, testData = data.randomSplit([0.7, 0.3])

randomForestModel = rf_instance.randomForestClassifier(data, trainingData)

predictions = randomForestModel.transform(testData)

predictions.select("predictedLabel", "classe", "features").show(95, False)

print(getError())