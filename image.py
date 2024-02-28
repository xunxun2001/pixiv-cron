class Image:
    def __init__(self, title, user_name, date, page_url, small_url, big_url, rank):
        self.title = title
        self.user_name = user_name
        self.date = date
        self.page_url = page_url
        self.small_url = small_url
        self.big_url = big_url
        self.rank = rank

    def __str__(self):
        return f"![]({self.small_url}) **#{self.rank}** [{self.title}]({self.page_url}) [Download]({self.big_url})"

    def __eq__(self, other):
        if not isinstance(other, Image):
            return False
        return (self.rank == other.rank and
                self.title == other.title and
                self.user_name == other.user_name and
                self.date == other.date and
                self.page_url == other.page_url and
                self.small_url == other.small_url and
                self.big_url == other.big_url)

    def __hash__(self):
        return hash((self.title, self.user_name, self.date, self.page_url, self.small_url, self.big_url,  self.rank))
