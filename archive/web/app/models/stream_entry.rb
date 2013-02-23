class StreamEntry < ActiveRecord::Base

  belongs_to :user
  belongs_to :article

  attr_accessible :weightning, :read

end