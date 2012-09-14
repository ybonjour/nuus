class User < ActiveRecord::Base

  has_many :stream_entries
  has_many :articles, :through => :stream_entries

  attr_accessible :email, :password, :password_confirmation
  has_secure_password
  validates :password, :presence => true, :on => :create
  
end
