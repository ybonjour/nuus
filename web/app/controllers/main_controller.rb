class MainController < ApplicationController

  def stream

    if logged_out?
      redirect_to :controller => :sessions, :action => :new
    end

  end

end
