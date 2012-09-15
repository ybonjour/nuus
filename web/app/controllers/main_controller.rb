class MainController < ApplicationController

  def stream

    if logged_out?
      redirect_to log_in_path
    end

  end

end
