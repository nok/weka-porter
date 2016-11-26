import os
from weka_weca import Porter

porter = Porter(language='java')
file_path = os.path.join('data', 'weather_data.txt')
result = porter.port(file_path, method_name='classify')
print(result)

"""
public static String classify(String outlook, bool windy, float humidity) {
    if (outlook == "sunny") {
        if (humidity <= 75) {
            return "yes";
        }
        else if (humidity > 75) {
            return "no";
        }
    }
    else if (outlook == "overcast") {
        return "yes";
    }
    else if (outlook == "rainy") {
        if (windy == true) {
            return "no";
        }
        else if (windy == false) {
            return "yes";
        }
    }
}
"""
