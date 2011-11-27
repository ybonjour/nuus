class CreateFeed < ActiveRecord::Migration
  def change
    create_table :feed do |t|

      t.timestamps
    end
  end
end
