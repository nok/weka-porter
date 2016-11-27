from weka_porter import Porter


porter = Porter(language='java')

result = porter.port('weather_data.txt', method_name='classify')
print(result)

"""
public static String classify(String outlook, boolean windy, double humidity) {
    if (outlook.equals("sunny")) {
        if (humidity <= 75) {
            return "yes";
        }
        else if (humidity > 75) {
            return "no";
        }
    }
    else if (outlook.equals("overcast")) {
        return "yes";
    }
    else if (outlook.equals("rainy")) {
        if (windy == true) {
            return "no";
        }
        else if (windy == false) {
            return "yes";
        }
    }
    return null;
}
"""

result = porter.port('weather_num_data.txt', method_name='classify_num')
print(result)

"""
public static int classify_num(String outlook, boolean windy, double humidity) {
    if (outlook.equals("sunny")) {
        if (humidity <= 75) {
            return 1;
        }
        else if (humidity > 75) {
            return -1;
        }
    }
    else if (outlook.equals("overcast")) {
        return 1;
    }
    else if (outlook.equals("rainy")) {
        if (windy == true) {
            return -1;
        }
        else if (windy == false) {
            return 1;
        }
    }
    return null;
}
"""