class Article < ActiveRecord::Base

  has_many :users, :through => :stream_entries

  attr_accessible :content, :language, :title, :updated

end