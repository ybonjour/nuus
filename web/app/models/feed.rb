class Feed < ActiveRecord::Base
  
  set_table_name 'feed'
  
  validates :url,   :presence => true
  validates :title, :presence => true
  
end
