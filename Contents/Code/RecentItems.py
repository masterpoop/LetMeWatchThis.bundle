import datetimeimport cerealizerclass BrowsedItems(object):	def __init__(self):			self.items = []		pass			def add(self, mediaInfo, providerURLs, path):			self.items.append([mediaInfo, providerURLs, path])				while (len(self.items) > 50):			self.items.pop(0)			def get(self, url):			# Look through each of our items and see if any of them has a URL		# which matches the passed in URL.		result = [elem for elem in self.items if url in elem[1]]		if (len(result) > 0):			return [result[0][0], result[0][2]]		else:			return None	def __str__(self):			return str(self.items)			class ViewedItems(object):	def __init__(self):			self.items = []			def add(self, mediainfo, path, keep):		# The last element of the path will contain the URL actually played.		played_url = path[-1]['url']				#Log('Trying to add item :' + played_url + ' to recently played list.')				result = [elem for elem in self.items if played_url == elem[2]]				if (len(result) <= 0):			self.items.insert(0,[mediainfo, path, played_url])		else:			# FIXME: Update last accessed time.			pass				#while (len(self.items) > keep):		#	self.items.pop()			def has_been_watched(self, url):			result = [elem for elem in self.items if url == elem[2]]				return(len(result) > 0)			def get(self, tv_mode=None, num_to_show=None):			ret_items = []				for item in self.items:					if (item[0].type == 'movie'):				ret_items.append(item)							else:							# Work out whether the item should be added to the list.				if (tv_mode is None or tv_mode == 'Episode'):					ret_items.append(item)				elif (tv_mode == 'Season'):									# See if we already have an entry for this show and season.					#					# First, do we have a show name and season to do comparison?					if (item[0].show_name is None or item[0].season is None):											# Don't have, can't compare, so add it in.						ret_items.append(item)											else:											result = [elem for elem in ret_items if (elem[0].show_name == item[0].show_name and elem[0].season == item[0].season)]												# If we don't have an existing item, add ourselves in. Otherwise, ignore it.						if (len(result) <= 0):							ret_items.append(item)									elif (tv_mode == 'Show'):								# See if we already have an entry for this show.					#					# First, do we have a show name to do comparison?					if (item[0].show_name is None or item[0].season is None):											# Don't have, can't compare, so add it in.						ret_items.append(item)											else:											result = [elem for elem in ret_items if (elem[0].show_name == item[0].show_name)]												# If we don't have an existing item, add ourselves in. Otherwise, ignore it.						if (len(result) <= 0):							ret_items.append(item)										# Do we have enough entries?			if (num_to_show and len(ret_items) >= num_to_show):				break					return ret_items					def __len__(self):			return len(self.items)		class FavouriteItems(object):	SORT_DEFAULT = 1	SORT_MRU = 2	SORT_ALPHABETICAL = 3		def __init__(self):			self.items = []			def add(self, mediainfo, path):		#Log('Trying to add item :' + str(mediainfo) + ' to favourites.')				result = None			if (mediainfo.type == 'tv' and mediainfo.season is not None):			result = [elem for elem in self.items if elem.mediainfo.id == mediainfo.id and elem.mediainfo.season == mediainfo.season]		else:			result = [elem for elem in self.items if (elem.mediainfo.id == mediainfo.id) and elem.mediainfo.season is None]				if (len(result) <= 0):			self.items.insert(0, FavouriteItem(mediainfo, path))		else:			# FIXME: Update last accessed time.			pass					def get(self, sort=None):			if (sort is None or sort == FavouriteItems.SORT_DEFAULT):			return self.items		elif (sort == FavouriteItems.SORT_ALPHABETICAL):			return sorted(self.items, key=lambda x: x.mediainfo.title)		elif (sort == FavouriteItems.SORT_ALPHABETICAL):			return sorted(self.items, key=lambda x: x.mediainfo.title)		else:			return self.items				def remove(self, mediainfo):			if (mediainfo.type == 'tv' and mediainfo.season is not None):			items_to_remove = [elem for elem in self.items if elem.mediainfo.id == mediainfo.id and elem.mediainfo.season == mediainfo.season]		else:			items_to_remove = [elem for elem in self.items if (elem.mediainfo.id == mediainfo.id) and elem.mediainfo.season is None]				for item in items_to_remove:			self.items.remove(item)			def __len__(self):			return len(self.items)		class FavouriteItem(Object):	def __init__(self, mediainfo, path):			self.mediainfo = mediainfo		self.path = path		self.date_added = datetime.datetime.utcnow()		self.date_last_used = self.date_added		self.new_item_check = False		self.items = None		self.date_last_item_check = Nonecerealizer.register(BrowsedItems)cerealizer.register(ViewedItems)cerealizer.register(FavouriteItems)cerealizer.register(FavouriteItem)