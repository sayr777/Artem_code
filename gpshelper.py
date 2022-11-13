

class GpsHelper():
	def run(self):
		#Request permissions on Android
		if platform == 'android':
			from android.permissions import Permission, request_permissions
			def callback(permission, results):
				if all([res for res in results]):
					print('Got all permissions')
				else:
					print('Did not get all permissions')

			request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], callback)
		
		#Configure GPS
		if platform == 'android' or platform == 'ios':
			from plyer import gps
			gps.start(minTime=1000, minDistance=0)
