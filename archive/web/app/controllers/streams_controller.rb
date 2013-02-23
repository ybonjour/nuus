class StreamsController < ApplicationController
  
  def index

    if logged_out?
      head :forbidden
      return
    end

    render :json => current_user.articles

  end
  
end