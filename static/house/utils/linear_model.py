from sklearn.linear_model import LinearRegression
import numpy

def linear_model_main(x_parameter, y_parameter, predoct_value):
    linear_reg = LinearRegression()
    linear_reg.fit(x_parameter,y_parameter)

    predict_value = numpy.array([predoct_value]).reshape(-1,1)
    predict_outcome = linear_reg.predict(predict_value)
    return predict_outcome

if __name__ == '__main__':
    x_data = [[4],[8],[9],[8],[7],[12]]
    y_data = [9,19,23,22,15,25]
    predict_value = 6
    predict_outcome = linear_model_main(x_data,y_data,predict_value)
    print("预测结果：",predict_outcome)