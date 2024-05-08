import requests
from vehicle_manager.utils import haversine_distance

class Vehicle:
    def __init__(self, id=None, name=None, model=None, year=None, color=None, price=None, latitude=None,
                 longitude=None):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"


class VehicleManager:
    def __init__(self, url):
        self.url = url

    def get_vehicles(self):
        response = requests.get(self.url + "/vehicles")
        return [Vehicle(**vehicle) for vehicle in response.json()]

    def filter_vehicles(self, params):
        vehicles = self.get_vehicles()
        filtered_vehicles = [vehicle for vehicle in vehicles if
                             all(getattr(vehicle, key) == value for key, value in params.items())]
        return filtered_vehicles

    def get_vehicle(self, vehicle_id):
        response = requests.get(self.url + f"/vehicles/{vehicle_id}")
        return Vehicle(**response.json())

    def add_vehicle(self, vehicle):
        vehicle_dict = vehicle.__dict__.copy()
        del vehicle_dict['id']
        response = requests.post(self.url + "/vehicles", json=vehicle_dict)
        return Vehicle(**response.json())

    def update_vehicle(self, vehicle):
        response = requests.put(self.url + f"/vehicles/{vehicle.id}", json=vehicle.__dict__)
        return Vehicle(**response.json())

    def delete_vehicle(self, id):
        response = requests.delete(self.url + f"/vehicles/{id}")
        return response.status_code == 204

    def get_distance(self, id1, id2):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)

        return haversine_distance(vehicle1.latitude, vehicle1.longitude, vehicle2.latitude, vehicle2.longitude)

    def get_nearest_vehicle(self, id):
        vehicle1 = self.get_vehicle(id)
        all_vehicles = self.get_vehicles()
        min_distance = float('inf')
        nearest_vehicle = None

        for vehicle2 in all_vehicles:
            if vehicle2.id == id:
                continue
            distance = haversine_distance(vehicle1.latitude, vehicle1.longitude, vehicle2.latitude,
                                               vehicle2.longitude)
            if distance <= min_distance:
                min_distance = distance
                nearest_vehicle = vehicle2
        return nearest_vehicle


if __name__ == "__main__":
    manager = VehicleManager(url="https://test.tspb.su/test-task")

    print(manager.get_vehicles())
    print(manager.filter_vehicles(params={"name": "Toyota"}))
    print(manager.get_vehicle(vehicle_id=1))
    print(manager.add_vehicle(
        vehicle=Vehicle(
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
        )
    ))
    print(manager.update_vehicle(
        vehicle=Vehicle(
            id=1,
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
        )
    ))
    print(manager.delete_vehicle(id=1))
    print(manager.get_distance(id1=1, id2=2))
    print(manager.get_nearest_vehicle(id=1))
