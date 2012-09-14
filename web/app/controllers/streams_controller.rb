class StreamsController < ApplicationController
  
  def index

    if current_user.nil?
      redirect_to :controller=>"main"
      return
    end

    @articles = current_user.articles

    respond_to do |format|
      format.json { render :json => @articles }
    end

  end
  
end