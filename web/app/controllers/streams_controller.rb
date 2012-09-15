class StreamsController < ApplicationController
  
  def index

    if logged_out?
      head :forbidden
      return
    end

    @articles = current_user.articles

    respond_to do |format|
      format.json { render :json => @articles }
    end

  end
  
end