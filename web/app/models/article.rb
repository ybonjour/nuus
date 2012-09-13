class Article < ActiveRecord::Base

  attr_accessible :content, :language, :title, :updated

end