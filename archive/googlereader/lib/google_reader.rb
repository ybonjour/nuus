require 'rubygems'
require 'httparty'

class GoogleReader
  include HTTParty
  base_uri 'www.google.com:443'
  default_params :output => 'json'
  
  def initialize(email, password)
    @email = email
    @password = password
    self.class.headers 'Authorization' => 'GoogleLogin auth=' + auth
  end
  
  def get_user_info
    self.class.get('/reader/api/0/user-info')
  end
  
  def get_feeds
    self.class.get('/reader/api/0/subscription/list')
  end
  
  private
  def auth
    @auth ||= authenticate["Auth"]
  end
  
  def authenticate
    result = self.class.get('/accounts/ClientLogin', :query => {
        :accountType => 'GOOGLE',
        :Email => @email,
        :Passwd => @password,
        :service => 'reader',
        :source => 'nuus-0.0.1'
      })

    @authentication = Hash.new
    result.each_line do |l|
        key_and_value = l.split("=")
        @authentication[key_and_value[0]] = key_and_value[1]
    end

    @authentication
  end
end
